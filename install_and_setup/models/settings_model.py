import json
from dataclasses import dataclass
from typing import Optional
from install_and_setup.config import CONFIG_JSON


@dataclass
class Settings:
    steam_inventory_link: str = ""
    discord_webhook_url: str = ""


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

    def save(self, settings: Settings) -> None:
        data = {
            "steam_inventory_link": settings.steam_inventory_link,
            "discord_webhook_url": settings.discord_webhook_url,
        }
        CONFIG_JSON.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
