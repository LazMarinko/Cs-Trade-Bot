# install_and_setup/config.py
from pathlib import Path
import os
import sys

APP_TITLE = "CS Trade Bot Installer"
WINDOW_WIDTH = 980
WINDOW_HEIGHT = 640

# 👇 Folder name for your app under AppData
APP_NAME = "CsTradeBot"

# Optional toggle for testing (writes config next to your script)
DEBUG_WRITE_TO_CWD = False


def _user_config_base() -> Path:
    """Return OS-specific per-user config base directory."""
    if sys.platform.startswith("win"):
        # Example → C:\Users\<User>\AppData\Roaming\CsTradeBot
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
    elif sys.platform == "darwin":
        # Example → ~/Library/Application Support/CsTradeBot
        base = Path.home() / "Library" / "Application Support"
    else:
        # Example → ~/.config/CsTradeBot
        base = Path(os.getenv("XDG_CONFIG_HOME", Path.home() / ".config"))
    return base


def _resolve_config_dir() -> Path:
    """Return the full config directory path."""
    if DEBUG_WRITE_TO_CWD or os.getenv("CSTB_DEBUG_CWD") == "1":
        return Path.cwd() / APP_NAME
    return _user_config_base() / APP_NAME


# 🔧 Create and expose the path
CONFIG_DIR: Path = _resolve_config_dir()
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CONFIG_JSON: Path = CONFIG_DIR / "config.json"
CHROME_PROFILE_PATH = r"C:\Temp\NewProfile"