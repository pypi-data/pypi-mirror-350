import typer
import os
import tomli_w
from rich.text import Text
from rich import print
from rich.prompt import Prompt
from typing import Optional
from datetime import datetime, timezone, time

from vodo.config import load_config

app = typer.Typer()


@app.command()
def tasks(
    done: bool = typer.Option(False, help="Include completed tasks"),
    plaintext: bool = typer.Option(
        False, "--plaintext", "-p", help="Print without formatting or colours"
    ),
):
    """List all tasks with priority and due date"""
    from vodo.api import list_tasks
    from vodo.ui import render_priority, render_due_date
    from rich.console import Console
    from rich.table import Table

    console = Console()
    table = Table(show_header=True, header_style="bold magenta", title="Current Tasks")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Priority", style="white")
    table.add_column("Due Date", style="white")

    if not plaintext:
        for task in list_tasks():
            priority_bar = render_priority(task.priority or 0)
            due_text = render_due_date(task.due_date)
            title_text = Text()
            if task.done:
                title_text.append("✔ ", style="green")
            title_text.append(task.title)
            if not done and task.done:
                continue

            table.add_row(str(task.id), title_text, priority_bar, due_text)

        console.print(table)
        raise typer.Exit()

    typer.echo("Current Tasks:")
    for task in list_tasks():
        due_text = render_due_date(task.due_date)
        if not done and task.done:
            continue
        typer.echo(f"{task.id}: {task.title}, priority:{task.priority}, due:{due_text}")
    raise typer.Exit()


@app.command()
def view(
    id: int,
    plaintext: bool = typer.Option(
        False, "--plaintext", "-p", help="Print without formatting or colours"
    ),
):
    """View a task"""
    from vodo.api import get_task
    from vodo.ui import render_priority, render_due_date
    from rich.console import Console
    from rich.table import Table

    task = get_task(id)

    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="cyan", no_wrap=True)
    table.add_column("Title", style="bold")
    table.add_column("Priority", style="white")
    table.add_column("Due Date", style="white")

    priority_bar = render_priority(task.priority or 0)
    due_text = render_due_date(task.due_date)
    title_text = Text()
    if not plaintext:
        if task.done:
            title_text.append("✔ ", style="green")
        title_text.append(task.title)

        table.add_row(str(task.id), title_text, priority_bar, due_text)

        console.print(table)
        raise typer.Exit()

    typer.echo(f"{task.id}: {task.title}, priority:{task.priority}, due:{due_text}")
    raise typer.Exit()


@app.command()
def add(
    title: str,
    description: Optional[str] = typer.Option(
        None, "--description", "-d", help="Task description"
    ),
    priority: int = typer.Option(
        1, "--priority", "-p", min=1, max=5, help="Task priority (1–5)"
    ),
    due_date: Optional[str] = typer.Option(
        None, "--due", help="Due date in YYYY-MM-DD format"
    ),
):
    """Add a new task"""
    from vodo.api import create_task

    if due_date:
        try:
            if ":" in due_date:
                # full datetime format: YYYY-MM-DD:HH:MM:SS
                date_part, time_part = due_date.split(":", 1)
                full_str = f"{date_part} {time_part.replace(':', ':', 2)}"
                full_datetime = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
            else:
                # fallback to midnight
                full_datetime = datetime.strptime(due_date, "%Y-%m-%d")
                full_datetime = datetime.combine(full_datetime.date(), time(0, 0, 0))

            full_datetime = full_datetime.replace(tzinfo=timezone.utc)
            due_date = full_datetime.isoformat().replace("+00:00", "Z")

        except ValueError:
            typer.echo(
                "❌ Invalid due date. Use YYYY-MM-DD or YYYY-MM-DD:HH:MM:SS", err=True
            )
            raise typer.Exit(code=1)

    task = create_task(
        title=title, description=description, priority=priority, due_date=due_date
    )

    typer.echo(f" Created task: [{task.id}] {task.title}")
    raise typer.Exit()


@app.command()
def edit(id: int):
    """Edit an existing task"""
    from vodo.api import get_task, update_task

    task = get_task(id)
    if not task:
        typer.echo(f"❌ Task with ID {id} not found.")
        raise typer.Exit(code=1)

    typer.echo(
        f"📝 Editing task [{task.id}]: {task.title}\n Press Enter to accept the current value."
    )

    new_title = Prompt.ask("Title", default=task.title)
    new_description = Prompt.ask("Description", default=task.description or "")
    new_priority_str = Prompt.ask("Priority (1–5)", default=str(task.priority or 1))
    new_due_date_str = Prompt.ask(
        "Due Date (YYYY-MM-DD or YYYY-MM-DD:HH:MM:SS)",
        default=task.due_date.strftime("%Y-%m-%d:%H:%M:%S")
        if task.due_date and task.due_date.year > 1
        else "",
    )

    # Parse fields
    try:
        new_priority = int(new_priority_str)
        if not 1 <= new_priority <= 5:
            raise ValueError
    except ValueError:
        typer.echo("❌ Invalid priority. Must be an integer between 1 and 5.")
        raise typer.Exit(code=1)

    due_date = None
    if new_due_date_str:
        try:
            if ":" in new_due_date_str:
                # full datetime
                date_part, time_part = new_due_date_str.split(":", 1)
                full_str = f"{date_part} {time_part.replace(':', ':', 2)}"
                due_date = datetime.strptime(full_str, "%Y-%m-%d %H:%M:%S")
            elif new_due_date_str == "":
                due_date = task.due_date
            else:
                # date only
                due_date = datetime.strptime(new_due_date_str, "%Y-%m-%d")
                due_date = datetime.combine(due_date.date(), datetime.min.time())

            due_date = due_date.replace(tzinfo=timezone.utc)
            due_date = due_date.isoformat().replace("+00:00", "Z")
        except ValueError:
            typer.echo("❌ Invalid due date format.")
            raise typer.Exit(code=1)

    updated = update_task(
        id=id,
        title=new_title,
        description=new_description,
        priority=new_priority,
        due_date=due_date,
    )

    typer.echo(f"✅ Updated task [{updated.id}]: {updated.title}")


@app.command()
def delete(task_id: int):
    from vodo.api import delete_task

    delete_task(task_id)
    typer.echo(f"Task {task_id} deleted.")


@app.command()
def done(task_id: int):
    """Mark a task as done"""
    from vodo.api import mark_task_done

    mark_task_done(task_id)
    typer.echo(f"Task {task_id} marked as done.")


@app.command()
def open(task_id: int):
    """Open a task in the browser"""
    print(f"Opening task {task_id}")
    config = load_config()
    url = config.get("api_url")
    typer.launch(f"{url}/tasks/{task_id}")


@app.command()
def setup(
    url: str = typer.Option(
        None,
        "--url",
        prompt="What is the base url of your instance? (include https://)",
    ),
    api_key: str = typer.Option(
        None,
        "--api_key",
        prompt="What is the api key for your instance? (Entry will be hidden)",
        hide_input=True,
    ),
):
    """Link a vikunja instance to vodo"""
    if not url.startswith("https://"):
        print("The instance url must include https://")
    config_data = {"api_url": f"{url}/api/v1", "token": api_key}

    config_path = os.path.expanduser("~/.config/vikunja/config.toml")
    if os.path.exists(config_path):
        print(
            "Configuration file already exists. Edit it at ~/.config/vikunja/config.toml"
        )
        raise typer.Exit(code=1)
    confirm = Prompt.ask(
        "These values will be written to ~/.config/vikunja/config.toml. Is that okay? (y/n)"
    )
    if confirm == "y":
        with open(config_path, "wb") as f:
            tomli_w.dump(config_data, f)
        print("Configuration file written")
    elif confirm == "n":
        print("Configuration file not written. Exiting.")
        raise typer.Abort()
    else:
        print("Confirmation not complete. Exiting.")
        raise typer.Exit()


if __name__ == "__main__":
    app()
