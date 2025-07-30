
from .inputs import Inputs
from .chromesettings import ChromeSettings
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import random

class Login():
    
            
    def __init__(self, chromesettings:ChromeSettings,inputs_instance:Inputs):
        
        self.chromesettings = chromesettings
        self.inputs_instance = inputs_instance
        
            
    def loginpage_interaction(self):
        
        """Opens the sign up page and sends credentials."""
        
        self.chromesettings.driver.get("https://secure.reed.co.uk/login?state=hKFo2SB6a0ludTZFdW8zNmRNUXR6bWJsUFFfeEg3bTdQaW1ZOKFupWxvZ2luo3RpZNkgazc3dE9sbktIb3Y2N1IyeDNuekZ3WTBPa2xwTXQ3c3ijY2lk2SBUS2JBVXhQRUFEWEFYZGYyN05tWUp2MEtnNmFEZnJkdA&client=TKbAUxPEADXAXdf27NmYJv0Kg6aDfrdt&protocol=oauth2&scope=openid%20profile%20email%20offline_access&redirect_uri=https%3A%2F%2Fwww.reed.co.uk%2Fauthentication%2Flogin%2Fcallback&audience=https%3A%2F%2Fwww.reed.co.uk%2F&response_type=code&response_mode=query&nonce=a2pJRGxmYTVSdFA4MGNCNlFlMFhxVjY0MWNMQXFYTkkyMnRmaHpOTkotZw%3D%3D&code_challenge=iwsfbRafIlFXcvUcGPk_sNu65V148bDShu1QCMC4SKM&code_challenge_method=S256&auth0Client=eyJuYW1lIjoiYXV0aDAtc3BhLWpzIiwidmVyc2lvbiI6IjIuMS4zIn0%3D")

        
        time.sleep(10)
        email_bar = self.chromesettings.driver.find_element(By.ID, "signin_email")
        time.sleep(self.chromesettings.random_time)
        email_bar.send_keys(self.inputs_instance.email + Keys.ENTER)


        password_bar = self.chromesettings.driver.find_element(By.ID, "signin_password")
        time.sleep(self.chromesettings.random_time)
        password_bar.send_keys(self.inputs_instance.password)


        continue_button = self.chromesettings.driver.find_element(By.ID, "signin_button")
        time.sleep(self.chromesettings.random_time)
        continue_button.click()
        
         
        time.sleep(20)
        accept_button = self.chromesettings.driver.find_element(
        By.XPATH,"/html/body/div[2]/div[2]/div/div/div[2]/div/div/button"
        )
        accept_button.click()
        
        
    