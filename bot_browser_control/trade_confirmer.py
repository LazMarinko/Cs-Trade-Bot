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


    def take_screenshot(self):
        # Load the image
        self.driver.save_screenshot('image.png')
        image_path = "image.png"  # Replace with your image path
        image = Image.open(image_path)

        # Define crop coordinates
        top_left_x = 452
        top_left_y = 6
        width = 938
        height = 914
        bottom_right_x = top_left_x + width
        bottom_right_y = top_left_y + height

        # Crop the image
        cropped_image = image.crop((top_left_x, top_left_y, bottom_right_x, bottom_right_y))

        current_url = self.get_url()

        # Save the cropped image
        cropped_image.save("cropped_image.png")
        webhook = DiscordWebhook(current_url)
        webhook.run()
        #cropped_image.show()

    def trade_constuctor(self):
        try:
            wait = WebDriverWait(self.driver, 15)

            my_inventory_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="inventory_select_your_inventory"]'))
            )
            my_inventory_button.click()

            my_item = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f'/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[7]/div[1]/div[{self.item_index}]/div'))
            )
            my_item.click()

            other_inventory_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="inventory_select_their_inventory"]'))
            )
            other_inventory_button.click()

            for index in self.index_tuple:
                their_item = wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f"/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[8]/div[1]/div[{index}]/div"))
                )
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


