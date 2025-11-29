# ui_and_scraper/close_ui/close_model.py
import random
import subprocess
import time
import threading

from bot_browser_control.bot import TradeBot  # adjust if your path is different


class CloseModel:
    """
    Model responsible for running the TradeBot in repeated cycles,
    until the provided stop_event is set.
    """

    def __init__(self, selected_index: int):
        self.selected_index = selected_index

    def run_bot_cycles(self, stop_event: threading.Event):
        """
        Loop:
          - kill Chrome
          - run TradeBot
          - wait 1 hour +/- 25%
        until stop_event is set.
        """
        while not stop_event.is_set():
            try:
                # Kill all existing Chrome processes
                try:
                    subprocess.call("taskkill /F /IM chrome.exe /T", shell=True)
                except Exception as e:
                    print(f"[CloseModel] Chrome kill error: {e}")

                # Let Chrome shut down
                time.sleep(2)

                if stop_event.is_set():
                    try:
                        subprocess.call("taskkill /F /IM chrome.exe /T", shell=True)
                        break
                    except Exception as e:
                        print(f"[CloseModel] Chrome kill error: {e}")
                        break

                print("🔁 Running bot cycle...")
                bot = TradeBot(self.selected_index)
                bot.run()

                # Wait between cycles with jitter
                delay_seconds = 3600 * random.uniform(0.75, 1.25)
                print(f"[CloseModel] Sleeping for {delay_seconds:.0f} seconds")

                # Sleep in chunks so we can react to stop_event faster
                slept = 0.0
                chunk = 1.0
                while slept < delay_seconds and not stop_event.is_set():
                    time.sleep(chunk)
                    slept += chunk

            except Exception as e:
                print(f"❌ Exception during bot cycle: {e}")
                # continue the loop unless stop was requested
