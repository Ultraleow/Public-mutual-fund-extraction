import pandas as pd
import time
import undetected_chromedriver as uc
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

def get_chrome_driver():
    try:
        # Try local ChromeDriver (Windows)
        driver_path = r"chromedriver.exe"
        service = Service(driver_path)
        driver = webdriver.Chrome(service=service)
        print("✅ Using normal Chrome (Windows)")
        return driver

    except Exception as e:
        print(f"⚠️ Normal Chrome (Windows) failed: {e}")

        try:
            # Try Docker/Linux ChromeDriver
            driver_path = r"/app/chromedriver"
            service = Service(driver_path)
            driver = webdriver.Chrome(service=service)
            print("✅ Using normal Chrome (Linux)")
            return driver

        except Exception as e:
            print(f"⚠️ Normal Chrome (Linux) failed: {e}")

            try:
                # Use undetected_chromedriver
                driver_path = r"/app/chromedriver"
                opt = uc.ChromeOptions()

                opt.add_argument("--no-sandbox")
                opt.add_argument("--start-maximized")
                opt.add_argument("--window-size=1200,800")
                opt.add_argument("--disable-extensions")
                opt.add_argument("--disable-application-cache")
                opt.add_argument("--disable-gpu")
                opt.add_argument("--disable-setuid-sandbox")
                opt.add_argument("--disable-dev-shm-usage")
                opt.add_argument("--headless")  # Enable/disable as needed

                driver = uc.Chrome(driver_executable_path=driver_path, options=opt)
                print("✅ Using undetected Chrome")

                return driver

            except Exception as e:
                print(f"❌ All Chrome drivers failed: {e}")
                return None  # Return None if everything fails