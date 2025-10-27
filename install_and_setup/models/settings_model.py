import json
from dataclasses import dataclass
from typing import Optional
from install_and_setup.config import CONFIG_JSON


@dataclass
class Settings:
    steam_inventory_link: str = ""
    discord_webhook_url: str = ""
    min_profit: float = 1.0
    max_profit: float = 1.0
    min_value: float = 0.0


class SettingsModel:

    def load(self) -> Optional[Settings]:
        if not CONFIG_JSON.exists():
            return None
        try:
            with open(CONFIG_JSON, "r", encoding="utf-8") as f:
                data = json.load(f)
            return Settings(**data)
        except Exception:
            return None

    def initial_save(self, settings: Settings) -> None:
        data = {
            "steam_inventory_link": settings.steam_inventory_link,
            "discord_webhook_url": settings.discord_webhook_url,
        }
        CONFIG_JSON.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    # ✅ Updated final save: converts percents into multipliers/ratios
    def final_save_trade_settings(
            self,
            min_profit_percent: float,
            max_profit_percent: float,
            min_target_item_percent: float,
    ) -> None:
        # Merge with existing file if present
        try:
            existing = {}
            if CONFIG_JSON.exists():
                with open(CONFIG_JSON, "r", encoding="utf-8") as f:
                    existing = json.load(f) or {}
        except Exception:
            existing = {}

        # Convert profit % → multiplier (e.g. 4 → 1.04)
        # Convert value % → decimal ratio (e.g. 60 → 0.6)
        existing["min_profit_multiplier"] = 1 + (min_profit_percent / 100)
        existing["max_profit_multiplier"] = 1 + (max_profit_percent / 100)
        existing["min_target_item_ratio"] = min_target_item_percent / 100

        CONFIG_JSON.parent.mkdir(parents=True, exist_ok=True)
        CONFIG_JSON.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
