from typer.testing import CliRunner
from vodo.main import app

runner = CliRunner()


def test_tasks():
    result = runner.invoke(app, ["tasks", "--plaintext"])
    assert result.exit_code == 0
    assert "priority:" in result.stdout


def test_add():
    result = runner.invoke(
        app,
        ["add", "-d", "test", "-p", 3, "--due", "2025-01-01", "test"],
    )
    assert result.exit_code == 0
    assert "test" in result.stdout
