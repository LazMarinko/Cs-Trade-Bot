from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TradeChecker:
    def __init__(self, driver, item_index):
        """
        Initializes TradeChecker with an existing WebDriver session.
        """
        self.driver = driver  # Use the already opened driver
        self.item_index = item_index - 1  # Convert 1-based to 0-based index

    def find_item_price(self):
        """Finds and prints the price of the selected trade item."""
        try:
            wait = WebDriverWait(self.driver, 10)

            # **Wait for the inventory container to load**
            inventory_container = wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@id, 'inventory_')]"))
            )

            # **Find all item divs inside the inventory container**
            items = inventory_container.find_elements(By.XPATH, "./div[contains(@id, '730_2')]")

            if self.item_index >= len(items):
                print(f"❌ Error: Selected item index {self.item_index + 1} is out of range.")
                return

            selected_item = items[self.item_index]  # **Select the correct Nth item**

            # **Find the price indicator within the selected item**
            try:
                price_element = selected_item.find_element(By.XPATH, ".//div[contains(@class, 'priceIndicator')]")
                price = price_element.text.strip()
                print(f"✅ Price of selected item: {price}")
            except Exception:
                print("⚠️ Price indicator not found for the selected item.")

        except Exception as e:
            print(f"❌ Error finding item price: {e}")

    def run(self):
        """Runs the price checking process."""
        self.find_item_price()
