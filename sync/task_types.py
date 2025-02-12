from collections.abc import Callable
from datetime import date, datetime
from typing import Any, NamedTuple


class Task(NamedTuple):
    """A CalDAV task."""

    uid: str
    summary: str
    description: str
    due: date | datetime | None = None
    priority: int = 0


type CalDAVCallback = Callable[[Task], None]
type TaskSource = Callable[[dict[str, Any], CalDAVCallback], None]
