from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time

driver = webdriver.Chrome()

try:
    driver.get("https://toolsqa.com")
    driver.execute_script("alert('Site opened!')")
    time.sleep(5)
    driver.switch_to.alert.accept()

    try:
        menu = driver.find_element("xpath", "//span[contains(text(), 'DEMO SITES')]")
        menu.click()
        driver.execute_script("alert('Clicked DEMO SITES!')")
    except NoSuchElementException:
        print("ELEMENT NOT FOUND")  
        driver.execute_script("alert('Element not found!')")
    
    time.sleep(5)
    driver.switch_to.alert.accept()

    driver.execute_script("alert('Site will be closed soon....')")
    time.sleep(5)
    driver.switch_to.alert.accept()

finally:
    driver.quit()