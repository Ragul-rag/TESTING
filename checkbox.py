from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://www.ironspider.ca/forms/checkradio.htm")
driver.maximize_window()
time.sleep(2)

checkboxes = driver.find_elements(By.XPATH, '//*[@name="color"]')

for box in checkboxes:
    if not box.is_selected():
        box.click()
print(" All checkboxes selected")

time.sleep(1)

for box in checkboxes:
    if box.get_attribute("value").lower() != "red" and box.is_selected():
        box.click()
print(" Deselected all except 'Red'")

time.sleep(5)
driver.quit()
