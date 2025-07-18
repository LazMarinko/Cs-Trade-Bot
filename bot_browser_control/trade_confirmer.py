from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
from discord.webhook import DiscordWebhook

class TradeConfirmer:
    def __init__(self, item_index, index_tuple, driver):
        self.driver = driver
        self.item_index = item_index
        self.index_tuple = index_tuple

    def find_all_inventories(self):
        inventory_containers = self.driver.find_elements(By.CSS_SELECTOR, "div[id^='inventory_'][id$='730_2']")
        inventory_container_id_list = []
        for inventory_container in inventory_containers:
            inventory_container_id_list.append(inventory_container.get_attribute('id'))
        return inventory_container_id_list

    def take_screenshot(self):
        # Load the image
        self.driver.save_screenshot('image.png')


        current_url = self.get_url()

        # Save the cropped imag
        webhook = DiscordWebhook(current_url)
        webhook.run()
        #cropped_image.show()

    def trade_constuctor(self):
        try:
            wait = WebDriverWait(self.driver, 15)

            inventory_container_id_list = self.find_all_inventories()

            user_inventory_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="inventory_select_your_inventory"]'))
            )
            user_inventory_button.click()

            user_inventory = self.driver.find_element(By.CSS_SELECTOR, f"#{inventory_container_id_list[0]}")
            user_items = user_inventory.find_elements(By.CSS_SELECTOR, '.item')[:16]
            user_items[self.item_index - 1].click()

            other_inventory_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="inventory_select_their_inventory"]'))
            )
            other_inventory_button.click()

            other_inventory = self.driver.find_element(By.CSS_SELECTOR, f"#{inventory_container_id_list[1]}")
            their_items = other_inventory.find_elements(By.CSS_SELECTOR, '.item')[:16]
            for index in self.index_tuple:
                their_item = their_items[index - 1]
                their_item.click()

            time.sleep(1.5)
            self.take_screenshot()
            time.sleep(5)

        except Exception as e:
            print(e)

    def get_url(self):
        current_url = self.driver.current_url
        return current_url


    def run(self):
        self.trade_constuctor()


