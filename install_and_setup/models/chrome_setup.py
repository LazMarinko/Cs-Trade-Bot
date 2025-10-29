import os
import time
import threading
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChromeSetupModel:
    """
    Non-blocking Chrome runner model.
    Controller calls start() to launch, polls is_running(), and can call stop().
    """

    def __init__(self, profile_path: str):
        self.profile_path = profile_path
        self._thread: Optional[threading.Thread] = None
        self._stop_evt = threading.Event()
        self._driver: Optional[webdriver.Chrome] = None
        self._last_error: Optional[str] = None

    # ---- Public API ----
    def start(self) -> bool:
        """Start Chrome in a background thread. Returns False if already running."""
        if self.is_running():
            return False
        self._stop_evt.clear()
        self._last_error = None
        self._thread = threading.Thread(target=self._run, name="ChromeSetupThread", daemon=True)
        self._thread.start()
        return True

    def stop(self):
        """Signal the runner to close Chrome and stop the thread."""
        self._stop_evt.set()

    def is_running(self) -> bool:
        """True if background thread is alive (Chrome presumed open)."""
        return self._thread is not None and self._thread.is_alive()

    def last_error(self) -> Optional[str]:
        return self._last_error

    # ---- Worker ----
    def _run(self):
        try:
            # Ensure profile dir exists
            os.makedirs(self.profile_path, exist_ok=True)

            # Chrome options
            options = webdriver.ChromeOptions()
            options.add_argument(f"--user-data-dir={self.profile_path}")
            options.add_argument("--profile-directory=Default")
            options.add_argument("--start-maximized")

            # Optional: reduce 'automation' banner
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)

            # Launch Chrome (downloads matching driver if needed)
            self._driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()),
                options=options
            )

            self._driver.get("https://steamcommunity.com/login")

            # Keep Chrome open until stop requested
            while not self._stop_evt.is_set():
                time.sleep(0.5)

        except Exception as e:
            self._last_error = str(e)
        finally:
            # Clean shutdown
            try:
                if self._driver is not None:
                    self._driver.quit()
            except Exception:
                pass
            self._driver = None
