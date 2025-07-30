import httpx
from vodo.config import get_auth_headers, BASE_URL
from vodo.models import Task
from datetime import datetime


def list_tasks() -> list[Task]:
    url = f"{BASE_URL}/tasks/all"
    headers = get_auth_headers()
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return [Task(**t) for t in response.json()]


def create_task(title: str, description: str, priority: int, due_date: str) -> Task:
    url = f"{BASE_URL}/projects/1/tasks"
    headers = get_auth_headers()
    data = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
    }
    response = httpx.put(url, headers=headers, json=data)
    response.raise_for_status()
    return Task(**response.json())


def get_task(task_id: int) -> Task:
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = get_auth_headers()
    response = httpx.get(url, headers=headers)
    response.raise_for_status()
    return Task(**response.json())


def update_task(
    id: int, title: str, description: str, priority: int, due_date: datetime
) -> Task:
    url = f"{BASE_URL}/tasks/{id}"
    headers = get_auth_headers()
    data = {
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
    }
    response = httpx.post(url, headers=headers, json=data)
    response.raise_for_status()
    return Task(**response.json())


def delete_task(task_id: int):
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = get_auth_headers()
    response = httpx.delete(url, headers=headers)
    response.raise_for_status()


def mark_task_done(task_id: int):
    url = f"{BASE_URL}/tasks/{task_id}"
    headers = get_auth_headers()
    data = {"done": True}
    response = httpx.post(url, headers=headers, json=data)
    response.raise_for_status()
