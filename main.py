from bot_browser_control.bot import TradeBot
from ui_and_scraper.ui import ItemSelectorUi
from ui_and_scraper.close_ui import CloseUI
import time
import threading


def run_bot():
    while not close_ui.is_stopped:
        bot = TradeBot(selected_index)
        bot.run()
        time.sleep(30)


if __name__ == "__main__":
    try:
        ui = ItemSelectorUi()
        ui.mainloop()

        # Store the selected index after UI closes
        selected_index = ui.selected_index + 1
        print(f"Final selected item index: {selected_index}")  # Debugging print

        close_ui = CloseUI(selected_index)
        close_ui.mainloop()
    except Exception as e:
        print(e)
