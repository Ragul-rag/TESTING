from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
import time

# Initialize the Chrome WebDriver
try:
    driver = webdriver.Chrome()

    # Try to open the website
    try:
        driver.get("https://example.com")
        driver.maximize_window()
        time.sleep(2)

        # Try to locate an element (like the <h1> tag on example.com)
        try:
            heading = driver.find_element(By.TAG_NAME, "h1")
            print("Page heading found:", heading.text)
        except Exception as e:
            print("Element not found:", e)

    except TimeoutException:
        print("Website loading timed out.")
    except WebDriverException as e:
        print("WebDriver error:", e)

except Exception as e:
    print("Error initializing WebDriver:", e)

finally:
    # Close the browser after test
    try:
        driver.quit()
    except:
        pass
