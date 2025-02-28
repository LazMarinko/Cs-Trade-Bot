from bot import TradeBot
from inv_scraper import get_inventory_items

if __name__ == "__main__":
    test_list = get_inventory_items()
    for i in test_list:
        new_string = str(i).strip("{}")
        print(new_string)
    # bot = TradeBot()  # Create an instance of TradeBot
    # bot.run()  # Run the bot