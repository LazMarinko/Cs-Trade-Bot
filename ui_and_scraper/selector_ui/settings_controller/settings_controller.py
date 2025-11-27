
from ui_and_scraper.selector_ui.settings_view.settings_view import SettingsView
from ui_and_scraper.selector_ui.settings_model.settings_model import SettingsModel


class SettingsController:
    def __init__(self, parent):
        self.model = SettingsModel()
        self.view = SettingsView(parent)

        self.view.on_close = self.handle_close
        self.view.on_save = self.handle_save

        # Load data into pages
        self.view.general_page_frame.load_values(
            self.model.get_inventory_link(),
            self.model.get_webhook(),
        )

        self.view.trade_page_frame.load_values(
            self.model.get_min_profit(),
            self.model.get_max_profit(),
            self.model.get_min_value(),
        )

    def handle_close(self):
        # nothing special yet
        pass

    def handle_save(self):
        # ---- read from UI ----
        inv = self.view.general_page_frame.get_inventory_link()
        webhook = self.view.general_page_frame.get_webhook()

        min_mult = self.view.trade_page_frame.get_min_profit_multiplier()
        max_mult = self.view.trade_page_frame.get_max_profit_multiplier()
        min_ratio = self.view.trade_page_frame.get_min_target_item_ratio()

        # ---- write into model ----
        self.model.set_inventory_link(inv)
        self.model.set_webhook(webhook)
        self.model.set_min_profit(min_mult)
        self.model.set_max_profit(max_mult)
        self.model.set_min_value(min_ratio)

        # ---- save to config.json ----
        self.model.save()
        print("[Settings] Saved to config.json")

        # optional: close settings after save
        self.view.destroy()
