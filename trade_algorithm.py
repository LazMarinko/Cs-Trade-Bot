from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from trade_confirmer import TradeConfirmer
import time


class TradeAlgorithm:
    def __init__(self, driver, selected_item_price, item_index):
        """Initialize TradeAlgorithm with WebDriver and selected item price."""
        self.driver = driver
        self.selected_item_price = float(selected_item_price.strip().replace('€', '').replace('$', ''))
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
            current_price = item_price
            print(current_price)
            combo_indexs = [(item_index,)]

            print(len(combo_indexs))
            pre_check_len = len(combo_indexs)
            while len(combo_indexs) < 5:
                failed_to_find_trade = False
                try:
                    for i in range(combo_indexs[0][0] + 1, len(items)):
                        time.sleep(3)
                        new_item_price = self.find_price(i)

                        new_price = current_price + new_item_price
                        print("New price:" + str(new_price))
                        print("Current price: " + str(current_price))

                        if self.selected_item_price * 1.035 < new_price < self.selected_item_price * 1.05:
                            print("Profit of 3-5% found at price: " + str(new_price))
                            new_combo_index = (i, *combo_indexs[0])
                            combo_indexs.insert(0, new_combo_index)
                            trade_confirmer = TradeConfirmer(self.item_index, combo_indexs[0], self.driver)
                            trade_confirmer.run()
                            trade_found = True
                            break
                        elif new_price < self.selected_item_price * 1.035:
                            current_price = new_price
                            print("No profit found yet proceeding, current price is: " + str(current_price))
                            new_combo_index = (i, *combo_indexs[0])
                            combo_indexs.insert(0, new_combo_index)
                            print("Current length of first element:" + str(len(combo_indexs)))
                            if len(combo_indexs) == 5:
                                break

                        else:
                            print("Invalid trade over 5% with price: " + str(new_price))
                            failed_to_find_trade = True



                except Exception as e:
                    print(e)

                if trade_found:
                    print("Trade found breaking")
                    break
                elif failed_to_find_trade:
                    print("Failed to find trade for current item checking new item")
                    break

                print("Total number of skins exceeded 5, trying a different item")
                combo_index_len = len(combo_indexs)
                to_be_yeated = combo_index_len - pre_check_len
                if combo_index_len == 1:
                    break
                else:
                    for i in range(0, to_be_yeated):
                        try:
                            combo_indexs.pop(i)
                        except IndexError:
                            break

            if trade_found:
                print("Trade found breaking")
                break


    def run(self):
        """Runs the trade algorithm."""
        print("🔍 Scanning inventory for tradeable items...")
        self.find_trade()
