import json
from typing import Any

import httpx
from dateparser.search import search_dates

from sync.task_types import CalDAVCallback, Task


def sync(config: dict[str, Any], add_task: CalDAVCallback) -> None:
    widget_state = httpx.post(
        "https://api.ozon.ru/composer-api.bx/page/json/v2?url=/my/orderlist",
        headers={"user-agent": "ozonapp_android/18.2.0+2538"},
        cookies={
            "__Secure-access-token": config["access_token"],
            "__Secure-refresh-token": config["refresh_token"],
        },
    ).json()["widgetStates"]["orderListApp-3573963-default-1"]
    data = json.loads(widget_state)["orderListApp"]

    for order in data:
        status = order["sections"][0]["status"]["name"].casefold()
        if "ожидает получения" in status:
            order_id = order["header"]["number"]

            due_date = None
            if dates := search_dates(status):
                due_date = dates[0][1].date()

            task = Task(
                uid=f"ozon-{order_id}",
                summary="Забрать заказ OZON",
                description=f"https://ozon.ru/my/orderdetails/?order={order_id}",
                due=due_date,
            )

            add_task(task)
