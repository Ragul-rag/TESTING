from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

driver = webdriver.Chrome()
driver.get("https://www.python.org")

downloads_link = driver.find_element(By.LINK_TEXT, "Downloads")

actions = ActionChains(driver)
actions.key_down(Keys.CONTROL).click(downloads_link).key_up(Keys.CONTROL).perform()
time.sleep(1)  

driver.switch_to.window(driver.window_handles[-1])
time.sleep(3)

print("Current URL:", driver.current_url)
assert "down" in driver.current_url.lower() 