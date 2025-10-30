import json
import os
from install_and_setup.config import CONFIG_JSON

def get_value_from_config(key):

    if not os.path.isfile(CONFIG_JSON):
        print(f"[Config] File not found at {CONFIG_JSON}")
        return None

    try:
        with open(CONFIG_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get(key)
    except json.JSONDecodeError:
        print(f"[Config] Corrupted config file at {CONFIG_JSON}")
        return None
    except Exception as e:
        print(f"[Config] Error reading config: {e}")
        return None
