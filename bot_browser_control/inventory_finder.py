from selenium.webdriver.common.by import By

def inventory_finder(driver, inventory_number):
    raw_inventory_containers = driver.find_elements(
        By.CSS_SELECTOR, "div[id^='inventory_'][id*='_730_']"
    )
    true_inventory_containers = []
    for raw_inventory_container in raw_inventory_containers:
        # consider any descendant; direct children may be empty shells
        descendants = raw_inventory_container.find_elements(By.XPATH, ".//*")
        if descendants:  # or: if len(descendants) > 0:
            true_inventory_containers.append(raw_inventory_container)

    return true_inventory_containers[inventory_number]