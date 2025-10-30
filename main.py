# main.py
from bot_browser_control.bot import TradeBot
from ui_and_scraper.ui import ItemSelectorUi
from ui_and_scraper.close_ui import CloseUI

# ← use your existing config.py that already defines these
from install_and_setup.config import CONFIG_JSON, CHROME_PROFILE_PATH

from install_and_setup.controllers.install_controller import InstallController  # adjust import if different

import os
import time
import subprocess
import sys


def files_ready() -> bool:
    """Both config file and Chrome profile folder must exist."""
    return os.path.isfile(CONFIG_JSON) and os.path.isdir(CHROME_PROFILE_PATH)


def run_install_ui() -> bool:
    """
    Run your install UI. Return True if inputs were saved successfully.
    We consider it successful if, when the window closes, both paths exist.
    """
    ctrl = InstallController()
    # If your controller exposes a start() or run() method, call that instead:
    try:
        # Option A: controller manages the view internally
        if hasattr(ctrl, "run"):
            ctrl.run()
        elif hasattr(ctrl, "start"):
            ctrl.start()
        else:
            # Fallback: show the controller's view mainloop
            ctrl.view.mainloop()
    except Exception as e:
        print(f"[Installer] Error during install UI: {e}")
        return False

    # Re-check after the wizard closes
    return files_ready()


def ensure_no_stale_chrome():
    """
    Safety cleanup so a leftover Chrome doesn’t block automation.
    Keep it *after* install (so CHROME_PROFILE_PATH is known).
    """
    try:
        # If you can target only your bot's Chrome, do that here.
        # Fallback: global kill to be safe (your original behavior).
        subprocess.call("taskkill /F /IM chrome.exe /T", shell=True)
    except Exception as e:
        print(f"[Startup] Chrome cleanup warning: {e}")


def main():
    # ---- Install/repair gate -------------------------------------------------
    if not files_ready():
        print("[Startup] Missing config or Chrome profile; launching installer...")
        if not run_install_ui():
            print("[Startup] Installer did not complete. Exiting.")
            sys.exit(1)

    # Optional: you could add a quick sanity re-check here or health checks.

    # ---- Safety: make sure no stale Chrome is holding locks ------------------
    ensure_no_stale_chrome()

    # ---- Your original flow --------------------------------------------------
    try:
        ui = ItemSelectorUi()
        ui.mainloop()

        selected_index = ui.selected_index + 1
        print(f"Final selected item index: {selected_index}")

        time.sleep(2)
        if selected_index is not None:
            close_ui = CloseUI(selected_index)
            close_ui.mainloop()
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
