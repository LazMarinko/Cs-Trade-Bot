from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bot_browser_control.trade_algorithm import TradeAlgorithm
from bot_browser_control.inventory_finder import inventory_finder


class TradeChecker:
    def __init__(self, driver, item_index):
        """Initializes TradeChecker with an existing WebDriver session."""
        self.driver = driver
        self.item_index = item_index  # Keep 1-based index for direct XPath selection

    def find_item_price(self):
        """Finds and prints the price of the selected trade item."""
        try:

            user_inventory_index = 0
            true_inventory_container = inventory_finder(self.driver, user_inventory_index)

            inventory_container_id = true_inventory_container.get_attribute('id')

            # Print the ID of the found inventory container for debugging purposes
            print(f"✅ Found inventory container with ID: {inventory_container_id}")

            inventory_container = self.driver.find_element(By.CSS_SELECTOR, f"#{inventory_container_id}")
            # 1) Grab ALL items first (no slicing here)
            item_divs = inventory_container.find_elements(
                By.CSS_SELECTOR, ".item, .itemHolder, [id^='item730_']"
            )

            while not item_divs:
                time.sleep(1)
                item_divs = inventory_container.find_elements(
                    By.CSS_SELECTOR, ".item, .itemHolder, [id^='item730_']"
                )

            # 2) Deduplicate by priceIndicator text
            unique_items = []
            seen_prices = set()

            for item in item_divs:
                try:
                    price_div = item.find_element(By.CLASS_NAME, "priceIndicator")
                    price_text = price_div.text.strip()
                except:
                    price_text = ""  # fallback if element is missing

                if price_text not in seen_prices:
                    seen_prices.add(price_text)
                    unique_items.append(item)

            # 3) Trim to your working limit
            unique_items = unique_items[:16]
            for item in unique_items:
                i = 1
                price_div = item.find_element(By.CLASS_NAME, "priceIndicator")
                price_text = price_div.text.strip()
                print(f"Item {i}: {price_text}")
                i += 1

            print(f"🔍 Found {len(unique_items)} unique items in inventory.")

            if not item_divs:
                print("❌ No items found in inventory. Exiting.")
                return

            # **Check if selected item index is within range**
            if self.item_index >= len(item_divs):
                print(f"❌ Selected item index {self.item_index} is out of range.")
                return


            # **Find price indicator**
            try:
                selected_item = unique_items[self.item_index - 1]
                print(f"✅ Selected item at index {self.item_index}.")

                # Try to find the price
                try:
                    price_element = selected_item.find_element(By.CLASS_NAME, "priceIndicator")
                    price = price_element.text.strip()
                    print(f"💰 Price of selected item: {price}")

                    # Try to click the other person's inventory button
                    try:
                        other_person_inv_button = self.driver.find_element(By.XPATH,
                                                                           '//*[@id="inventory_select_their_inventory"]')
                        other_person_inv_button.click()
                        time.sleep(2)

                        trade_alg = TradeAlgorithm(self.driver, price, self.item_index)
                        trade_alg.run()
                    except Exception as e:
                        print(f"⚠️ Could not click 'other inventory' button: {e}")

                except Exception:
                    print("⚠️ Price indicator not found for selected item.")

            except IndexError:
                print(f"❌ Invalid item index: {self.item_index}. Only {len(unique_items)} items found.")
        except Exception as e:
            print(f"❌ Error while selecting item: {e}")

    def run(self):
        """Runs the price checking process."""
        print("🔍 Running price check for selected item...")
        self.find_item_price()
