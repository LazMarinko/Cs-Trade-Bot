from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TradeChecker:
    def __init__(self, driver, item_index):
        """
        Initializes TradeChecker with an existing WebDriver session.
        """
        self.driver = driver  # Use the already opened driver
        self.item_index = item_index  # Use 1-based index for direct XPath selection

    def find_item_price(self):
        """Finds and prints the price of the selected trade item."""
        try:
            wait = WebDriverWait(self.driver, 10)

            # **Ensure the inventory container is loaded**
            inventory_container = wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]")
                )
            )
            print("✅ Inventory container found.")

            # **Construct XPath for the specific item**
            item_xpath = f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[7]/div[1]/div[{self.item_index}]/div"

            # **Locate the selected item**
            selected_item = wait.until(
                EC.presence_of_element_located((By.XPATH, item_xpath))
            )
            print(f"🔍 Found selected item at index {self.item_index}.")

            # **Find price indicator inside the selected item**
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
        print("🔍 Running price check for selected item...")
        self.find_item_price()
