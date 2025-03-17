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
        self.selected_index = None  # Variable to store the selected index

        # **Combo box starts with "Loading..."**
        self.items = ctk.CTkComboBox(self, values=["Loading..."], variable=self.selected_item)
        self.items.configure(width=175)
        self.items.pack(pady=10)

        # **Select button (Initially Disabled)**
        self.button = ctk.CTkButton(self, text="Select", command=self.select_item, state="disabled")
        self.button.pack(pady=20)

        # **Start item loading in a separate thread**
        self.load_items_thread = threading.Thread(target=self.load_items, daemon=True)
        self.load_items_thread.start()

        # **Handle UI Closing Properly**
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_items(self):
        """Runs the inventory scraper and updates the combo box when finished."""
        tradeable_items = get_inventory_items()  # Get tradeable items from scraper

        if not tradeable_items:
            item_list = ["No tradeable items found"]
        else:
            item_list = [f"{item['Item: ']} ({item['Exterior']})" for item in tradeable_items]

        # **Update the ComboBox with new items**
        if self.winfo_exists():  # Ensure the UI still exists before updating
            self.items.configure(values=item_list)
            self.selected_item.set(item_list[0])  # Select the first item automatically
            self.button.configure(state="normal")  # Enable the button after loading

    def select_item(self):
        """Save the selected item's index when the button is pressed and close UI."""
        all_items = self.items.cget("values")  # Get all items from the ComboBox
        selected_value = self.selected_item.get()  # Get the currently selected item

        if selected_value in all_items:
            self.selected_index = all_items.index(selected_value)  # Save the index
            print(f"✅ Selected item index: {self.selected_index}")  # Debugging print

        self.destroy()  # Properly close the UI

    def on_closing(self):
        """Handle UI closing properly to avoid freezing."""
        print("❌ UI is closing...")
        self.quit()  # Ensures all loops stop running
        self.destroy()  # Ensures all elements are closed
