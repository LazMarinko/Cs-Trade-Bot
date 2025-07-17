from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bot_browser_control.trade_algorithm import TradeAlgorithm


class TradeChecker:
    def __init__(self, driver, item_index):
        """Initializes TradeChecker with an existing WebDriver session."""
        self.driver = driver
        self.item_index = item_index  # Keep 1-based index for direct XPath selection

    def find_item_price(self):
        """Finds and prints the price of the selected trade item."""
        try:
            wait = WebDriverWait(self.driver, 15)  # Increased timeout to 15 sec

            # **Ensure the inventory container is loaded**
            print("🔍 Waiting for inventory container...")
            inventory_container = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]")
                )
            )
            print("✅ Inventory container found.")

            time.sleep(3)
            # Now safely find all item divs within inventory_container
            # Step 1: Find your inventory container
            inventory_container = self.driver.find_element(By.CSS_SELECTOR, '#inventory_76561198264077039_730_2')
            item_divs = inventory_container.find_elements(By.CSS_SELECTOR, '.item')[:16]

            while not item_divs:
                time.sleep(1)
                item_divs = inventory_container.find_elements(By.CSS_SELECTOR, '.item')

            print(f"🔍 Found {len(item_divs)} total items in inventory.")

            for i, item in enumerate(item_divs):
                try:
                    price_div = item.find_element(By.CLASS_NAME, "priceIndicator")
                    price = price_div.text.strip()
                except:
                    price = "No price found"
                print(f"Item {i + 1}: {price}")

            print(f"🔍 Found {len(item_divs)} total items in inventory.")

            if not item_divs:
                print("❌ No items found in inventory. Exiting.")
                return

            # **Check if selected item index is within range**
            if self.item_index >= len(item_divs):
                print(f"❌ Selected item index {self.item_index} is out of range.")
                return


            # **Find price indicator**
            try:
                selected_item = item_divs[self.item_index - 1]
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
                print(f"❌ Invalid item index: {self.item_index}. Only {len(item_divs)} items found.")
        except Exception as e:
            print(f"❌ Error while selecting item: {e}")

    def run(self):
        """Runs the price checking process."""
        print("🔍 Running price check for selected item...")
        self.find_item_price()
