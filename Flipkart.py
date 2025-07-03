from selenium import webdriver
from selenium.webdriver.common.options import ArgOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

driver=webdriver.Chrome()
driver.get("https://www.flipkart.com")
driver.maximize_window()
driver.find_element(By.CLASS_NAME,'Pke_EE').send_keys("Iphone 16")
driver.find_element(By.CLASS_NAME,'Pke_EE').send_keys(Keys.ENTER)
driver.find_element(By.CLASS_NAME,'KzDlHZ').click()
driver.switch_to.window(driver.window_handles[-1])
#driver.execute_script("window.scrollBy(0, 500)")
button = driver.find_element(By.CSS_SELECTOR, "button._2KpZ6l")
driver.execute_script("arguments[0].scrollIntoView();", button)
button.click()