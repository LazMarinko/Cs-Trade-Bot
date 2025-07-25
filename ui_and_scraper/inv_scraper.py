from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from webdriver_manager.chrome import ChromeDriverManager
import time

def get_inventory_items():

    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=C:\Temp\NewProfile")
    options.add_argument(r"--profile-directory=Default")
    options.add_experimental_option("detach", True)  # Optional: keep Chrome open after script ends
    #options.add_argument("--headless")
    options.add_argument("--start-maximized")
    # Initialize driver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://steamcommunity.com/profiles/76561198264077039/inventory#730")
    time.sleep(5)

    # Locate the dropdown and select the 3rd option
    dropdown = Select(driver.find_element("css selector", "#sortingMethod"))
    dropdown.select_by_index(2)
    print("print select index")
    time.sleep(5)
    tradeable_item_list = []

    try:
        inventory_container = driver.find_element(By.CSS_SELECTOR, "#inventories")
        items = inventory_container.find_elements(By.CSS_SELECTOR, ".item")

        tradeable_count = 0
        index = 0

        while tradeable_count < 10 and index < len(items):
            item = items[index]
            try:
                item.click()
                time.sleep(2)

                # Extract item name with retries
                item_name = ""
                retries = 10
                retry_clicks = 3
                while retries > 0:
                    try:
                        item_name_element = driver.find_element(By.CSS_SELECTOR, "#iteminfo0_content > div.item_desc_description > a.hover_item_name.custom_name")
                        item_name = item_name_element.text.strip()
                        if item_name:
                            break
                    except Exception:
                        pass

                    retries -= 1
                    time.sleep(0.5)

                    if retries == 5 and retry_clicks > 0:
                        item.click()
                        retry_clicks -= 1
                        time.sleep(2)

                if not item_name:
                    index += 1
                    continue

                # Extract item wear
                try:
                    wear_element = driver.find_element(By.CSS_SELECTOR, "#iteminfo0_item_descriptors > div:nth-child(1)")
                    wear_text = wear_element.text.strip()
                    if wear_text.startswith("Exterior: "):
                        wear_mapping = {
                            "Factory New": "FN",
                            "Minimal Wear": "MW",
                            "Field-Tested": "FT",
                            "Well-Worn": "WW",
                            "Battle-Scarred": "BS"
                        }
                        wear_initials = wear_mapping.get(wear_text.replace("Exterior: ", "").strip(), "N/A")
                    else:
                        wear_initials = "N/A"
                except Exception:
                    wear_initials = "N/A"

                # Extract trade restriction duration
                try:
                    trade_restriction_element = item.find_element(By.CLASS_NAME, "provisional_item_badge")
                    trade_restriction = trade_restriction_element.text.strip()
                except Exception:
                    trade_restriction = "No restriction"

                if trade_restriction == "No restriction":
                    tradeable_item_list.append({"Item: ": item_name, "Exterior": wear_initials})
                    tradeable_count += 1

                    # 🔥 **Print updated tradeable count every time a new item is added**
                    print(f"Tradeable items found: {tradeable_count}/10")

                index += 1
                time.sleep(1)

            except Exception as e:
                index += 1
                print(e)

    except Exception as e:
        print(e)

    driver.quit()
    return tradeable_item_list
