from bot_browser_control.bot import TradeBot
from ui_and_scraper.ui import ItemSelectorUi
from ui_and_scraper.close_ui import CloseUI
import time
import subprocess
import threading


if __name__ == "__main__":
    try:
        try:
            subprocess.call("taskkill /F /IM chrome.exe /T", shell=True)
        except Exception as e:
            print(e)
        ui = ItemSelectorUi()
        ui.mainloop()

        # Store the selected index after UI closes
        selected_index = ui.selected_index + 1
        print(f"Final selected item index: {selected_index}")  # Debugging print

        time.sleep(2)
        if selected_index is not None:
            close_ui = CloseUI(selected_index)
            close_ui.mainloop()
    except Exception as e:
        print(e)
