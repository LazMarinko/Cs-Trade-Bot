import customtkinter as ctk
import threading
from inv_scraper import get_inventory_items

class ItemSelectorUi(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Item Selector")
        self.geometry("400x300")

        # Label for the dropdown
        self.label = ctk.CTkLabel(self, text="Select item to trade:", font=("Helvetica", 14))
        self.label.pack(pady=10)

        # **CTk StringVar to hold selected item**
        self.selected_item = ctk.StringVar(value="Loading...")

        # **Combo box starts with "Loading..."**
        self.items = ctk.CTkComboBox(self, values=["Loading..."], variable=self.selected_item)
        self.items.configure(width = 175)
        self.items.pack(pady=10)

        # **Start item loading in a separate thread**
        self.load_items_thread = threading.Thread(target=self.load_items, daemon=True)
        self.load_items_thread.start()

    def load_items(self):
        """Runs the inventory scraper and updates the combo box when finished."""
        tradeable_items = get_inventory_items()  # Get tradeable items from scraper

        if not tradeable_items:
            item_list = ["No tradeable items found"]
        else:
            item_list = [f"{item['Item: ']} ({item['Exterior']})" for item in tradeable_items]

        # **Update the ComboBox with new items**
        self.items.configure(values=item_list)
        self.selected_item.set(item_list[0])  # Select the first item automatically

if __name__ == "__main__":
    app = ItemSelectorUi()
    app.mainloop()
