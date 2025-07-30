import os
import tomli

CONFIG_PATH = os.path.expanduser("~/.config/vikunja/config.toml")


def load_config():
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(f"Config file not found at {CONFIG_PATH}")
    with open(CONFIG_PATH, "rb") as f:
        return tomli.load(f)


_config = load_config()

BASE_URL = _config.get("api_url")
VIKUNJA_TOKEN = _config.get("token")
DUE_SOON_DAYS = _config.get("due_soon_days", 3)


def get_auth_headers():
    if not VIKUNJA_TOKEN:
        raise ValueError("No API token found in config file.")
    return {"Authorization": f"Bearer {VIKUNJA_TOKEN}"}
