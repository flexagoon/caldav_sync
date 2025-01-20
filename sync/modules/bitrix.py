from typing import Any

import httpx

from sync.task_types import CalDAVCallback, Task


def sync(config: dict[str, Any], callback: CalDAVCallback) -> None:
    tasks = httpx.post(
        f"https://{config["domain"]}/rest/{config["user_id"]}/{config["token"]}/tasks.task.list",
        json={
            "filter": {
                "RESPONSIBLE_ID": config["user_id"],
                "STAGE_ID": config["stage_id"],
            },
            "select": ["TITLE", "GROUP_ID"],
        },
    ).json()["result"]["tasks"]

    for task in tasks:
        callback(
            Task(
                uid=task["id"],
                summary=task["title"],
                description=f"https://{config["domain"]}/workgroups/group/{task["groupId"]}/tasks/task/view/{task["id"]}/",
            ),
        )
