from pathlib import Path

APP_TITLE = "CS Trade Bot • Setup"
WINDOW_WIDTH = 780
WINDOW_HEIGHT = 560

# Save next to the app, like your original script did
ROOT_DIR = Path(__file__).resolve().parent
CONFIG_JSON = ROOT_DIR / "config.json"

# Path to temp.py (launcher script you already have)
CHROME_PROFILE_PATH = r"C:\Temp\NewProfile"
