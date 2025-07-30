# Vodo

This is a simple command line interface for [vikunja](https://vikunja.io). It is recommended that you use a terminal that has support for nerd fonts and that you have a nerd font installed. I will work on a config option to remove all of the fancy display bells and whistles and just use text for everything, but this is not available at the moment.

![a screenshot of what the tool looks like](https://cdn.markpitblado.me/vodo-screenshot.png)

## Installation

`vodo` is available via [pypi](https://pypi.org)

```shell
pip install vodo
```

Or, if you are using [uv](https://docs.astral.sh/uv/)

```shell
uv tool install vodo
```

## Usage

The easiest way to see the available options is through the `--help` option. The high-level commands are listed below

| Command | Description                                                                   |
| ------- | ----------------------------------------------------------------------------- |
| tasks   | View all tasks. Use the `--done` option to show completed tasks               |
| view    | View a task by passing the task id as the argument                            |
| add     | Add a task using the title as an argument. Add other elements through options |
| edit    | Edit a task view the task id. Interactive.                                    |
| done    | Mark a task as complete via the task id.                                      |

## Configuration

The application expects there to be configuration variables available at `~/.config/vikunja/config.toml`. I will be adding options to add additional paths in the feature. The file should look like this.

```toml
api_url = "https://vikunja.example.com" # required
token = "your_api_token" # required
due_soon_days = 3 # optional
```

`due_soon_days` represents the number of days away a due date should be before being highlighted red.

## Contributing

Pull requests and issues are welcome. This repository uses the following:

- uv for package mangement
- ruff for python formatting and linting
- mdformat for markdown formatting
- pre-commit for hooks
