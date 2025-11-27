import json
from install_and_setup.config import CONFIG_JSON


class SettingsModel:
    """Loads and saves settings from config.json."""

    def __init__(self):
        with open(CONFIG_JSON, "r", encoding="utf-8") as f:
            self.config = json.load(f)

    # ===== Getters =====
    def get_inventory_link(self):
        return self.config.get("steam_inventory_link", "")

    def get_webhook(self):
        return self.config.get("discord_webhook_url", "")

    def get_min_profit(self):
        # e.g. 1.04
        return self.config.get("min_profit_multiplier", 1.0)

    def get_max_profit(self):
        # e.g. 1.08
        return self.config.get("max_profit_multiplier", 1.0)

    def get_min_value(self):
        # e.g. 0.6
        return self.config.get("min_target_item_ratio", 0.0)

    # ===== Setters (update in-memory config) =====
    def set_inventory_link(self, value: str):
        self.config["steam_inventory_link"] = value

    def set_webhook(self, value: str):
        self.config["discord_webhook_url"] = value

    def set_min_profit(self, multiplier: float):
        self.config["min_profit_multiplier"] = float(multiplier)

    def set_max_profit(self, multiplier: float):
        self.config["max_profit_multiplier"] = float(multiplier)

    def set_min_value(self, ratio: float):
        self.config["min_target_item_ratio"] = float(ratio)

    # ===== Persist to disk =====
    def save(self):
        with open(CONFIG_JSON, "w", encoding="utf-8") as f:
            json.dump(self.config, f, indent=2)
