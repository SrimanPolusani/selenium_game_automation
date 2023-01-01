# ----------------------Automating a game using Selenium----------------------

from selenium import webdriver
import time

from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By

chrome_driver_path = "../../../Downloads/chromedriver_win32/chromedriver.exe"
driver = webdriver.Chrome(chrome_driver_path)
driver.get("http://orteil.dashnet.org/experiments/cookie/")

# Clicking the cookie
cookie = driver.find_element(By.ID, "cookie")

# Collecting the ID of upgrade items
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + 5
five_min = time.time() + 60 * 5  # 5min

while True:
    cookie.click()

    # Every 5 sec:
    if time.time() > timeout:

        # Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        # Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        # Creating dictionary of store items and there prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        # Current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        # Finding upgrades that we are affordable currently
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        # Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        try:
            if not 3 < int(driver.find_element(By.CSS_SELECTOR, f"#{to_purchase_id} .amount").text):
                driver.find_element(By.ID, to_purchase_id).click()
        except NoSuchElementException:
            driver.find_element(By.ID, to_purchase_id).click()

        # 5 sec until the next check
        timeout = time.time() + 5

    # After 5 min terminate the game and print cookies per sec.
    if time.time() > five_min:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
