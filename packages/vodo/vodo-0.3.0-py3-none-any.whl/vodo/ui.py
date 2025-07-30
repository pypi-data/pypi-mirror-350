from datetime import datetime, timezone
from typing import Optional
from rich.text import Text

from vodo.config import DUE_SOON_DAYS


def render_priority(priority: int) -> Text:
    total_dots = 5
    filled = 0
    color = "dim"

    if priority in [1, 2]:
        filled = 1
        color = "green"
    elif priority == 3:
        filled = 3
        color = "yellow"
    elif priority in [4, 5]:
        filled = 5
        color = "red"

    text = Text()
    text.append("●" * filled, style=color)
    text.append("●" * (total_dots - filled), style="grey50")
    return text


def render_due_date(due: Optional[datetime]) -> Text:
    dt = datetime.fromisoformat(str(due).rstrip("Z")).replace(tzinfo=timezone.utc)
    if not due or dt == datetime(1, 1, 1, tzinfo=timezone.utc):
        return Text("—", style="dim")

    now = datetime.now(due.tzinfo) if due.tzinfo else datetime.now()
    days_left = (due - now).days

    if days_left < 0:
        return Text(due.strftime("%Y-%m-%d"), style="bold red")
    elif days_left < DUE_SOON_DAYS:
        return Text(due.strftime("%Y-%m-%d"), style="red")
    else:
        return Text(due.strftime("%Y-%m-%d"), style="green")
