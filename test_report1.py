import pytest
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from openpyxl import Workbook

wb = Workbook()
ws = wb.active
ws.title = "Test Logs"
ws.append(["Timestamp", "Level", "Message"])

def log_to_excel(level, message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    ws.append([timestamp, level, message])
    print(f"[{level}] {message}")

driver = webdriver.Chrome()
driver.maximize_window()

screenshot_file = ""

try:
    log_to_excel("INFO", "Opening ToolsQA website...")
    driver.get("https://www.toolsqa.com")
    time.sleep(3)

    log_to_excel("INFO", "Verifying title...")
    assert "Tools QA" in driver.title
    log_to_excel("PASS", "Title is correct.")

    log_to_excel("INFO", "Searching for 'Selenium'...")
    search_box = driver.find_element(By.XPATH, "//input[@placeholder='Search…']")
    search_box.send_keys("Selenium")
    time.sleep(1)
    search_box.send_keys(Keys.RETURN)
    log_to_excel("PASS", "Search submitted.")

except AssertionError:
    screenshot_file = "assertion_failed.png"
    driver.save_screenshot(screenshot_file)
    log_to_excel("FAIL", "Title mismatch. Screenshot saved.")
    pytest.fail("AssertionError")

except Exception as e:
    screenshot_file = f"{type(e).__name__}.png"
    driver.save_screenshot(screenshot_file)
    log_to_excel("ERROR", f"{type(e).__name__} occurred. Screenshot saved.")
    pytest.fail(type(e).__name__)

finally:
    driver.quit()
    log_to_excel("INFO", "Browser closed. Test complete.")
    wb.save("test_log.xlsx")

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    if rep.when == "call" and rep.failed:
        extra = getattr(rep, "extra", [])
        if screenshot_file and os.path.exists(screenshot_file):
            extra.append(pytest_html.extras.image(screenshot_file))
        if os.path.exists("test_log.xlsx"):
            extra.append(pytest_html.extras.text("See Excel file: test_log.xlsx", name="Excel Log"))
        rep.extra = extra

@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    global pytest_html
    pytest_html = config.pluginmanager.getplugin('html')