import pytest
import logging
import time
import os
from io import StringIO
import pytest_html
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

SCREENSHOT_DIR = r"C:\Users\snrag\OneDrive\Desktop\Project\screenshots"
EXCEL_LOG_PATH = r"C:\Users\snrag\OneDrive\Desktop\Project\test_login.xls"
WAIT_TIMEOUT = 20

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://opensource-demo.orangehrmlive.com/")
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        lambda d: d.execute_script("return document.readyState") == "complete")
    time.sleep(2)
    yield driver
    driver.quit()

def take_screenshot(driver, name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    path = os.path.join(SCREENSHOT_DIR, f"{name}.png")
    driver.save_screenshot(path)
    return path

def show_and_close_alert(driver, message):
    driver.execute_script(f"alert('{message}')")
    time.sleep(1)
    alert = driver.switch_to.alert
    alert_text = alert.text
    alert.accept()
    return alert_text

def login(driver, username, password):
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "username"))).clear()
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located((By.NAME, "password"))).clear()
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(3)

def logout(driver):
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "oxd-userdropdown-tab"))).click()
    WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Logout"))).click()
    time.sleep(3)

def save_logs_to_excel(log_data, filename):
    try:
        log_lines = [line for line in log_data.split('\n') if line.strip()]
        data = {"Timestamp": [], "Log Message": []}
        
        for line in log_lines:
            if " - " in line:
                timestamp, message = line.split(" - ", 1)
                data["Timestamp"].append(timestamp.strip())
                data["Log Message"].append(message.strip())
            else:
                data["Timestamp"].append("")
                data["Log Message"].append(line.strip())
        
        df = pd.DataFrame(data)
        df.to_excel(filename, index=False, engine='openpyxl')
        return True
    except Exception as e:
        print(f"Error saving Excel: {str(e)}")
        return False

def test_login_scenarios(driver, request):
    test_log = StringIO()
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler(test_log)
    handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logger.addHandler(handler)
    
    try:
        logger.info("TESTING VALID LOGIN")
        login(driver, "Admin", "admin123")
        
        WebDriverWait(driver, WAIT_TIMEOUT).until(EC.title_contains("OrangeHRM"))
        actual_title = driver.title
        expected_title = "OrangeHRM"
        assert actual_title == expected_title , 'NOT MATCHED'
        logger.info("LOGIN SUCCESS - Dashboard title verified")
        
        show_and_close_alert(driver, "LOGIN SUCCESSFUL")
        success_screenshot = take_screenshot(driver, "successful_login")
        logout(driver)

        logger.info("TESTING INVALID CREDENTIALS")
        login(driver, "Admin", "111111")
        
        error_msg = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located((By.CLASS_NAME, "oxd-alert-content-text"))).text
        logger.info(f"LOGIN FAILED - System message: {error_msg}")
        
        show_and_close_alert(driver, "INVALID CREDENTIALS")
        invalid_screenshot = take_screenshot(driver, "invalid_credentials")

        logger.info("TESTING EMPTY CREDENTIALS")
        driver.find_element(By.NAME, "username").clear()
        driver.find_element(By.NAME, "password").clear()
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        validation_errors = driver.find_elements(By.CLASS_NAME, "oxd-input-field-error-message")
        error_texts = [error.text for error in validation_errors]
        logger.info(f"EMPTY LOGIN ATTEMPT - Validation errors: {error_texts}")
        
        show_and_close_alert(driver, "EMPTY CREDENTIALS")
        empty_screenshot = take_screenshot(driver, "empty_credentials")

    finally:
        logger.removeHandler(handler)
        log_content = test_log.getvalue()
        
        if not save_logs_to_excel(log_content, EXCEL_LOG_PATH):
            print("Warning: Failed to save Excel logs")
        
        extra = getattr(request.node, "extra", [])
        extra.extend([
            pytest_html.extras.png(success_screenshot),
            pytest_html.extras.png(invalid_screenshot),
            pytest_html.extras.png(empty_screenshot),
            pytest_html.extras.text(log_content, name="Execution Log"),
            pytest_html.extras.html('<a href="test_login.xls">Download Excel Logs</a>')
        ])
        request.node.extra = extra