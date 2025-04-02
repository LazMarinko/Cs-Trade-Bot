from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random
from bot_browser_control.trade_checker import TradeChecker  # Import TradeChecker

class TradeBot:
    def __init__(self, item_number):
        """
        Initializes TradeBot with Chrome WebDriver and stores the selected item number.
        """
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"--user-data-dir=C:\Users\dragan\AppData\Local\Google\Chrome\User Data")
        options.add_argument(r"--profile-directory=Profile 1")
        #options.add_argument("--headless")
        #options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.forum_url = "https://steamcommunity.com/app/730/tradingforum/"
        self.clicked_posts = set()
        self.item_number = item_number  # Store selected item number

    def open_forum(self):
        """Opens the CS2 trade forum."""
        self.driver.get(self.forum_url)
        time.sleep(random.uniform(1, 3))

    def get_valid_elements(self):
        """Finds trade posts, skipping pinned ones."""
        time.sleep(random.uniform(2, 4))
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        container = soup.select_one('#forum_Trading_3381077_18446744073709551615_topiccontainer')

        if container:
            elements = container.find_all('div', id=lambda x: x and x.startswith(
                'forum_Trading_3381077_18446744073709551615_'))
            elements = elements[4:19]  # Skip first 3 pinned posts, limit to 16
            return [element.get('id') for element in elements]
        return []

    def click_random_element(self):
        """Selects and clicks a random trade post, avoiding duplicates."""
        post_ids = self.get_valid_elements()
        random.shuffle(post_ids)

        while post_ids:
            post_id = post_ids.pop()

            if post_id in self.clicked_posts:
                continue  # Skip already clicked posts

            try:
                post = self.driver.find_element(By.ID, post_id)
                time.sleep(random.uniform(1, 3))
                post.click()
                time.sleep(random.uniform(2, 4))

                self.clicked_posts.add(post_id)  # Mark as clicked

                time.sleep(4)
                try:
                    trade_offer_button = self.driver.find_element(By.XPATH,
                        '//*[@id="AppHubContent"]/div/div[1]/div[3]/div[1]/a')
                    trade_offer_button.click()
                    time.sleep(random.uniform(2, 4))

                    # Switch to the new trade offer tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(random.uniform(2, 4))
                    try:
                        active_app = self.driver.find_element(By.ID, 'appselect_activeapp')
                        if 'Counter-Strike 2' not in active_app.text:
                            active_app.click()
                            time.sleep(random.uniform(1, 3))
                            cs2_option = self.driver.find_element(By.XPATH,
                                                                  "//div[contains(text(), 'Counter-Strike 2')]")
                            cs2_option.click()
                            time.sleep(random.uniform(2, 4))
                    except Exception as e:
                        print(f"Error checking/selecting CS2: {e}")

                    # Ensure trade offer page is loaded before checking for the container
                    time.sleep(random.uniform(2, 4))
                    try:
                        trade_container = self.driver.find_element(By.CSS_SELECTOR, '#appselect_activeapp')
                        print("Trade container found.")
                    except Exception:
                        print("Trade container not found.")

                    # **Run TradeChecker on the selected item**
                    trade_checker = TradeChecker(self.driver, self.item_number)  # Pass driver and item number
                    trade_checker.run()  # Execute TradeChecker logic

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                except Exception as e:
                    print(f"No trade offer button found for post {post_id}: {e}")
                # Ensure CS2 is selected
                self.driver.back()
                time.sleep(random.uniform(2, 5))
                post_ids = self.get_valid_elements()
                random.shuffle(post_ids)
            except Exception as e:
                print(f"Error clicking post {post_id}: {e}")
                continue

    def run(self):
        """Runs the test_1."""
        self.open_forum()
        self.click_random_element()
        self.driver.quit()
