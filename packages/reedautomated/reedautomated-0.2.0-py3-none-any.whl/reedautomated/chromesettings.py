from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import timedelta


class ChromeSettings:

    def __init__(self):
        
        """Settings of the chrome browser."""
        

        # Create Chromeoptions instance
        self.options = webdriver.ChromeOptions()

        # Adding argument to disable the AutomationControlled flag
        self.options.add_argument("--disable-blink-features=AutomationControlled")
        self.options.add_argument("--headless")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)


        # Disabling password manager pop up
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
        }
        self.options.add_experimental_option("prefs", prefs)

        # Exclude the collection of enable-automation switches
        self.options.add_experimental_option("excludeSwitches", ["enable-automation"])

        # Turn-off userAutomationExtension
        self.options.add_experimental_option("useAutomationExtension", False)
        self.options.add_experimental_option("detach", True)

        # Setting the driver path and requesting a page
        self.driver = webdriver.Chrome(options=self.options)

        # Changing the property of the navigator value for webdriver to undefined
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.driver.set_window_size(1920, 1080)
    
        self.random_time = random.randrange(2, 11)
        self.loop_duration_time = timedelta(minutes=random.choice(range(15,30)))
        self.wait = WebDriverWait(self.driver, 10)
