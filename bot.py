from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import random


class TradeBot:
    def __init__(self):
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"--user-data-dir=C:\Users\dragan\AppData\Local\Google\Chrome\User Data")  # Corrected user data path
        options.add_argument(r"--profile-directory=Profile 1")  # Corrected profile name

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        self.forum_url = "https://steamcommunity.com/app/730/tradingforum/"
        self.clicked_posts = set()  # Store already clicked posts

    def open_forum(self):
        """Opens the CS2 trade forum."""
        self.driver.get(self.forum_url)
        time.sleep(random.uniform(1, 3))  # Increased wait time for elements to fully load

    def get_valid_elements(self):
        """Waits for elements to fully load and retrieves valid post IDs, skipping pinned posts."""
        time.sleep(random.uniform(2, 4))  # Ensure the page fully loads
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        container = soup.select_one('#forum_Trading_3381077_18446744073709551615_topiccontainer')
        print("Container found:" if container else "Container not found.")

        if container:
            elements = container.find_all('div', id=lambda x: x and x.startswith(
                'forum_Trading_3381077_18446744073709551615_'))
            elements = elements[4:19]  # Skip first 3 pinned posts and limit to 16
            return [element.get('id') for element in elements]
        else:
            print("Container not found.")
            return []

    def click_random_element(self):
        """Randomly selects and clicks an element inside the container, avoiding duplicates."""
        post_ids = self.get_valid_elements()
        random.shuffle(post_ids)  # Shuffle to make selection more human-like

        while post_ids:
            post_id = post_ids.pop()  # Select and remove a random post

            if post_id in self.clicked_posts:
                continue  # Skip if already clicked

            try:
                post = self.driver.find_element(By.ID, post_id)
                self.driver.execute_script("arguments[0].scrollIntoView();", post)
                time.sleep(random.uniform(1, 3))
                post.click()
                time.sleep(random.uniform(2, 4))  # Random delay for human-like behavior

                self.clicked_posts.add(post_id)  # Mark post as clicked

                # Check if CS2 is selected in #appselect_activeapp
                try:
                    active_app = self.driver.find_element(By.ID, 'appselect_activeapp')
                    if 'Counter-Strike 2' not in active_app.text:
                        active_app.click()
                        time.sleep(random.uniform(1, 3))  # Allow dropdown to appear
                        cs2_option = self.driver.find_element(By.XPATH, "//div[contains(text(), 'Counter-Strike 2')]")
                        cs2_option.click()
                        time.sleep(random.uniform(2, 4))  # Allow selection to process
                except Exception as e:
                    print(f"Error checking or selecting CS2: {e}")

                # Click the trade offer button if available
                try:
                    trade_offer_button = self.driver.find_element(By.CSS_SELECTOR,
                                                                  '#AppHubContent > div > div.leftcol > div.forum_topic_tradeoffer_area.forum_formarea_box > div.forum_topic_tradeoffer_button_ctn > a')
                    trade_offer_button.click()
                    time.sleep(random.uniform(2, 4))  # Allow time for the trade page to load

                    # Switch to the new trade offer tab
                    self.driver.switch_to.window(self.driver.window_handles[-1])
                    time.sleep(random.uniform(2, 4))  # Allow time for the trade page to load completely

                    # Ensure the trade offer page is fully loaded before checking for the container
                    time.sleep(random.uniform(2, 4))
                    try:
                        trade_container = self.driver.find_element(By.CSS_SELECTOR, '#appselect_activeapp')
                        print("Trade container found.")
                    except Exception:
                        print("Trade container not found.")
                except Exception:
                    print(f"No trade offer button found for post {post_id}")

                self.driver.back()
                time.sleep(random.uniform(2, 5))  # Random back delay
                post_ids = self.get_valid_elements()  # Refresh elements list after navigating back
                random.shuffle(post_ids)  # Shuffle again for variation
            except Exception as e:
                print(f"Error clicking post {post_id}: {e}")
                continue

    def run(self):
        """Runs the bot."""
        self.open_forum()
        self.click_random_element()
        self.driver.quit()
