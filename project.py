from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver=webdriver.Chrome()
driver.get('https://www.reliancedigital.in/?gad_source=1&gad_campaignid=1720209518&gbraid=0AAAAADthdYkPRT4FAPaH_tNIxGdTpfZF9&gclid=Cj0KCQjwjo7DBhCrARIsACWauSkG_kDndPyZXG5ycWdhea633j24WlgD6oarngK5yIGSfBbP1zkg5gMaAlXBEALw_wcB')
driver.maximize_window()
time.sleep(3)
driver.find_element(By.ID,"wzrk-cancel").click()