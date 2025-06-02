from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bot_browser_control.trade_confirmer import TradeConfirmer
import time


class TradeAlgorithm:
    def __init__(self, driver, selected_item_price, item_index):
        """Initialize TradeAlgorithm with WebDriver and selected item price."""
        self.driver = driver
        self.selected_item_price = float(selected_item_price.strip().replace('€', '').replace('$', ''))
        self.item_index = item_index
        new_combo_price = 0

    def find_price(self, item_index):
        """Find the price of an item at the given index."""
        try:
            item_xpath = f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[8]/div[1]/div[{item_index}]/div"
            item_element = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.XPATH, item_xpath))
            )

            price_element = item_element.find_element(By.XPATH, ".//div[contains(@class, 'priceIndicator')]")
            price_text = price_element.text.strip().replace("€", "").replace("$", "").strip()
            return float(price_text)

        except Exception:
            return None  # Return None if price not found

    def scan_inventory(self):
        """Scans the entire other person's inventory, prints all item prices."""
        try:
            # Wait for the inventory container to load
            # Ensure inventory_container is located correctly before this code:
            inventory_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="inventories"]'))
            )

            # Correct XPath relative to your previously found container
            items = inventory_container.find_elements(By.XPATH, "./div[8]/div[1]/div")
            print(f"Total items found: {len(items)}")

            index = 1
            suitable_items = []
            if items is not None:
                while index < len(items) + 1:
                    try:
                        item_price = self.find_price(index)

                        if item_price < self.selected_item_price and item_price > self.selected_item_price * 0.5:
                            suitable_items.append((index, item_price))

                        index += 1
                    except Exception as e:
                        print(e)
                        break

            print("Suitable item indexes:", suitable_items)
            return suitable_items

        except Exception as e:
            print(f"❌ Error scanning other inventory: {e}")

    def find_trade(self):
        """Find a trade with 3-5% profit using the fewest items possible."""
        all_items = self.scan_inventory()

        inventory_container = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="inventories"]'))
        )

        # Correct XPath relative to your previously found container
        items = inventory_container.find_elements(By.XPATH, "./div[8]/div[1]/div")

        trade_found = False
        for item_index, item_price in all_items:
            base_price = item_price
            base_combo = [(item_index,)]  # list of tuples to track combinations

            print(f"🔍 Starting base item index {item_index} with price {base_price}")

            def try_combos(combo, current_total, depth):
                nonlocal trade_found
                if depth == 5:
                    return

                start_index = combo[0] + 1
                for i in range(start_index, len(items)):
                    try:
                        item_xpath = f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[8]/div[1]/div[{i}]/div"
                        item_element = self.driver.find_element(By.XPATH, item_xpath)

                        price_element = item_element.find_element(By.XPATH,
                                                                  ".//div[contains(@class, 'priceIndicator')]")
                        price_text = price_element.text.strip().replace("€", "").replace("$", "").strip()
                        next_price = float(price_text)

                        new_total = current_total + next_price
                        new_combo = (i, *combo)

                        print(f"🧮 Trying combo {new_combo} with total {new_total:.2f}")

                        if self.selected_item_price * 1.04 <= new_total <= self.selected_item_price * 1.07:
                            print(f"✅ Profit combo found: {new_combo} = {new_total:.2f}")
                            trade_confirmer = TradeConfirmer(self.item_index, new_combo, self.driver)
                            trade_confirmer.run()
                            trade_found = True
                            return

                        elif new_total < self.selected_item_price * 1.04\
                                :
                            try_combos(new_combo, new_total, depth + 1)

                        if trade_found:
                            return

                    except Exception as e:
                        print(f"⚠️ Error checking item at index {i}: {e}")

            try_combos((item_index,), base_price, 1)

            if trade_found:
                print("🎉 Trade found. Exiting.")
                break

        if not trade_found:
            print("❌ No trade found within 3-5% profit range.")

    def run(self):
        """Runs the trade algorithm."""
        print("🔍 Scanning inventory for tradeable items...")
        self.find_trade()
