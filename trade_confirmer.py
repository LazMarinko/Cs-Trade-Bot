from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class TradeConfirmer:
    def __init__(self, item_index, index_list, driver):
        self.driver = driver
        self.item_index = item_index
        self.index_list = index_list


    def trade_constuctor(self):
        try:
            wait = WebDriverWait(self.driver, 15)

            my_inventory_button = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="inventory_select_your_inventory"]'))
            )
            my_inventory_button.click()

            my_item = self.driver.find_element_by_xpath(f'/html/body/div[1]/div[5]/div[3]/div[1]/div[3]/div[1]/div[1]/div[2]/div[6]/div[7]/div[1]/div[{self.item_index}]/div')
            my_item.click()


        except Exception as e:
            print(e)



    def run(self):
        self.trade_constuctor()


