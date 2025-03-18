from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from trade_confirmer import TradeConfirmer

class TradeAlgorithm:
    def __init__(self, driver, selected_item_price, item_index):
        """Initialize TradeAlgorithm with WebDriver and selected item price."""
        self.driver = driver
        self.selected_item_price = selected_item_price
        self.item_index = item_index
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
            inventory_container = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="inventories"]'))
            )

            items = inventory_container.find_elements(By.XPATH, "./div[2]/div[1]/div")
            print(f"Total items found: {len(items)}")

            index = 1
            suitable_items = []
            while index < 17:
                try:
                    item_xpath = f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[8]/div[1]/div[{index}]/div"
                    item_element = self.driver.find_element(By.XPATH, item_xpath)

                    price_element = item_element.find_element(By.XPATH, ".//div[contains(@class, 'priceIndicator')]")
                    price_text = price_element.text.strip().replace("€", "").replace("$", "").strip()
                    item_price = float(price_text)
                    formated_price = float(self.selected_item_price.strip().replace("€", ""))

                    if item_price < formated_price and item_price > formated_price * 0.5:
                        suitable_items.append((index, item_price))

                    index += 1
                except Exception as e:
                    print(e)

            print("Suitable item indexes:", suitable_items)
            return suitable_items

        except Exception as e:
            print(f"❌ Error scanning other inventory: {e}")

    def find_trade(self):
        """Find a trade with 3-5% profit using the fewest items possible."""
        all_items = self.scan_inventory()

        selected_item_price_float = float(self.selected_item_price.strip().replace('€', '').replace('$', '').strip())

        for item_index, item_price in all_items:
            current_price_float = float(item_price) if isinstance(item_price, str) else item_price

            for i in range(item_index + 1, item_index + 5):
                item_xpath = f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[8]/div[1]/div[{i}]/div"
                item_element = self.driver.find_element(By.XPATH, item_xpath)

                price_element = item_element.find_element(By.XPATH, ".//div[contains(@class, 'priceIndicator')]")
                price_text = price_element.text.strip().replace('€', '').replace('$', '').strip()
                next_item_price_float = float(price_text)

                current_price = item_price + next_item_price_float  # Ensure both are floats

                if 1.03 * selected_item_price_float <= current_price <= 1.05 * selected_item_price_float:
                    print(f"✅ Profit trade found: {current_price:.2f}")
                    index_list = []
                    index_list.append(item_index)
                    index_list.append(i)
                    trade_confirmer = TradeConfirmer(self.driver,self.item_index, index_list)
                    trade_confirmer.run()


                elif current_price < 1.03 * selected_item_price_float:
                    print(f"🔄 No suitable trade yet, total price: {current_price:.2f}")
                else:
                    print("⚠️ No suitable trade found (price too high).")

    def run(self):
        """Runs the trade algorithm."""
        print("🔍 Scanning inventory for tradeable items...")
        self.find_trade()
