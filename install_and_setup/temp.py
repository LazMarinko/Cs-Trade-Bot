import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def run_initial_chrome_setup():
    # Target path for the user profile
    profile_path = r"C:\Temp\NewProfile"

    # Create the directory if it doesn't exist
    if not os.path.exists(profile_path):
        os.makedirs(profile_path)
        print(f"✅ Created profile directory at {profile_path}")
    else:
        print(f"⚠️ Profile directory already exists at {profile_path}")

    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument(f"--user-data-dir={profile_path}")
    options.add_argument("--profile-directory=Default")  # Use the Default profile inside that folder
    options.add_argument("--start-maximized")

    # Optional: Disable automation flag for better compatibility
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)

    # Launch Chrome
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get("https://steamcommunity.com/login")
    print("🟢 Chrome opened with fresh profile. Please log into Steam and install any needed extensions.")

    # Let user interact
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("🔴 Chrome setup closed.")
        driver.quit()


if __name__ == "__main__":
    run_initial_chrome_setup()
