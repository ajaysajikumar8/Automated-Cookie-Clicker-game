from selenium import webdriver
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "E:\chromedriver_win32\chromedriver.exe"
driver = webdriver.Chrome(executable_path=chrome_driver_path)

driver.get(url="http://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.CSS_SELECTOR, "div #cookie")

timeout = time.time() + 5
five_min = time.time() + 5*60

# get item ids
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]


while True:
    cookie.click()
    
    if time.time() > timeout:    
        #get prices for item
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        #get individual price of the item
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",",""))
                item_prices.append(cost)

        # create dictionary for store item and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #get current money
        money_element = driver.find_element(By.CSS_SELECTOR, "div #money").text
        if "," in money_element:
            money_element = money_element.replace(",","")
        cookie_count = int(money_element)

        #find upgrades which we can afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                affordable_upgrades[cost] = id

        #purchase the most expensive affordable upgrades
        highest_price_affordable_upgrade = max(affordable_upgrades)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]
        
        driver.find_element(By.ID, to_purchase_id).click()
        
        timeout = time.time() + 5

    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID, "cps")
        print(cookie_per_sec.text)
        break

driver.quit()
