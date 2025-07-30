from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Task(BaseModel):
    id: int
    title: str
    description: Optional[str]
    done: bool
    priority: Optional[int] = 0
    due_date: Optional[datetime] = None
