# ui_and_scraper/item_selector_model.py
import threading
from ui_and_scraper.inv_scraper import get_inventory_items


class ItemSelectorModel:

    def load_items(self):
        tradeable_items = get_inventory_items()

        if not tradeable_items:
            # No tradeable items – controller can decide how to handle this
            return []

        # Same formatting you had before
        item_list = [
            f"{item['Item: ']} ({item['Exterior']})"
            for item in tradeable_items
        ]
        return item_list
