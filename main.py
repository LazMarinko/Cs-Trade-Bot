from bot import TradeBot
from inv_scraper import get_inventory_items
from ui import ItemSelectorUi

if __name__ == "__main__":
    ui = ItemSelectorUi()
    ui.mainloop()

    # Store the selected index after UI closes
    selected_index = ui.selected_index
    print(f"Final selected item index: {selected_index}")  # Debugging print

    bot = TradeBot(selected_index)  # Create an instance of TradeBot
    bot.run()  # Run the bot
