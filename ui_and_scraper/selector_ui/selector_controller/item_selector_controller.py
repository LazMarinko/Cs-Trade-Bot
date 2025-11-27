# ui_and_scraper/item_selector_controller.py
import threading
from ui_and_scraper.selector_ui.selector_model.item_selector_model import ItemSelectorModel
from ui_and_scraper.selector_ui.selector_view.item_selector_view import ItemSelectorView
from ui_and_scraper.selector_ui.settings_controller.settings_controller import SettingsController


class ItemSelectorController:
    """
    Controller: wires model + view, handles threading, selection, and lifecycle.
    """

    def __init__(self, view: ItemSelectorView | None = None, model: ItemSelectorModel | None = None):
        self.model = model or ItemSelectorModel()
        self.view = view or ItemSelectorView()

        self.selected_index: int | None = None

        # Wire callbacks
        self.view.on_select = self.handle_select
        self.view.on_close = self.handle_close
        self.view.on_settings = self.handle_settings

        # Start in loading state
        self.view.set_loading()

        # Load items on a background thread
        self._load_thread = threading.Thread(target=self._load_items_worker, daemon=True)
        self._load_thread.start()

    # ==== Threaded loading ====

    def _load_items_worker(self):
        item_labels = self.model.load_items()

        def update_ui():
            if not self.view.winfo_exists():
                return

            # Load the items into the UI
            self.view.set_items(item_labels)

            # Enable the "Select" button now that items exist
            self.view.button.configure(state="normal")

            # Enable the settings cog as well
            self.view.enable_settings()

        self.view.after(0, update_ui)

    # ==== Callbacks from the view ====

    def handle_select(self):
        self.selected_index = self.view.get_selected_index()
        print(f"✅ Selected item index: {self.selected_index}")
        if self.view.winfo_exists():
            self.view.destroy()

    def handle_close(self):
        print("❌ UI is closing...")
        if self.view.winfo_exists():
            self.view.destroy()

    def handle_settings(self):
        # Re-open if closed
        if not hasattr(self, "settings_controller") or not self.settings_controller.view.winfo_exists():
            self.settings_controller = SettingsController(parent=self.view)
        else:
            # If it's already open, just focus it
            self.settings_controller.view.focus()

    # ==== Public API ====

    def run(self) -> int | None:
        """
        Start the UI loop. Blocks until the window is closed.
        Returns the selected index (or None).
        """
        self.view.mainloop()
        return self.selected_index
