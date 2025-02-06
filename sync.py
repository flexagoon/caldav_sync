import functools
import tomllib
from pathlib import Path

import caldav

from sync.modules import bitrix, homework, ozon
from sync.task_types import Task, TaskSource


def add_task(task: Task, cal: caldav.Calendar) -> None:
    try:
        cal.todo_by_uid(task.uid)
    except caldav.error.NotFoundError:  # type: ignore[attr-defined]
        cal.save_todo(**task._asdict())
        print(f"[{cal.name}] Adding task: {task.summary}")


MODULES: dict[str, TaskSource] = {
    "Homework": homework.sync,
    "Work": bitrix.sync,
    "Errands": ozon.sync,
}


if __name__ == "__main__":
    with Path("config.toml").open("rb") as f:
        config = tomllib.load(f)

    with caldav.DAVClient(**config["caldav"]) as client:
        principal = client.principal()
        for calendar in principal.calendars():
            if calendar.name in MODULES:
                print(f"[{calendar.name}] Syncing")
                source = MODULES[calendar.name]
                module_config = config["modules"][calendar.name]
                callback = functools.partial(add_task, cal=calendar)
                source(module_config, callback)
