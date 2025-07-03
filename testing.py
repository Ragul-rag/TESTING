from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.alert import Alert
import time

driver = webdriver.Chrome()

driver.get("https://www.google.com") 
time.sleep(2)

driver.execute_script("alert('This is an ALERT MESSAGE');")
time.sleep(2)

alert = Alert(driver)
print("Alert text:", alert.text)
alert.accept()  

driver.get("https://www.python.org")
time.sleep(2)

driver.maximize_window()

downloads_link = driver.find_element(By.LINK_TEXT, "Downloads")
downloads_link.click()
time.sleep(2)

driver.back()
time.sleep(2)

driver.forward()
time.sleep(2)

driver.refresh()
time.sleep(2)

print("All navigation methods demonstrated successfully!")

driver.quit()