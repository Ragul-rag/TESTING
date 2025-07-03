import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

driver = webdriver.Chrome()
driver.get("https://letcode.in/dropdowns")
driver.maximize_window()
time.sleep(3)

dropdown_element = driver.find_element(By.ID, "fruits")
dropdown_element.click()
time.sleep(1)

dropdown = Select(dropdown_element)
dropdown.select_by_visible_text("Mango")
time.sleep(1)

option = dropdown.first_selected_option
print("Selected option is:", option.text)

time.sleep(3)
driver.quit()
