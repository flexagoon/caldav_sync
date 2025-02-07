from datetime import datetime
from typing import Any

import httpx

from sync.task_types import CalDAVCallback, Task

FORMATIVE_TASK_TYPE = 202


def sync(config: dict[str, Any], add_task: CalDAVCallback) -> None:
    with httpx.Client() as client:
        client.post(f"https://{config["domain"]}/ajaxauthorize", data=config["auth"])

        tasks = client.get(
            f"https://{config["domain"]}/journal-api-lms-action",
            params={
                "action": "lms.get_tasks",
                "study_year": "2024/2025",
                "status": "assigned",
            },
        ).json()["result"]["tasks"]

    for task in tasks:
        if task["course_id"] in config["course_blacklist"]:
            continue

        add_task(
            Task(
                uid=str(task["id"]),
                summary=task["name"],
                description=f"https://{config["domain"]}/journal-course-action/pg.task?task_id={task["id"]}",
                due=datetime.strptime(
                    task["deadline_at"],
                    "%Y-%m-%d %H:%M:%S",
                ).astimezone(),
                priority=(0 if task["type_evaluation"] == FORMATIVE_TASK_TYPE else 1),
            ),
        )
