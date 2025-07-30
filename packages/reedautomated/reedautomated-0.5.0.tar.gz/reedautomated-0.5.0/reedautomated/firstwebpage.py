from .chromesettings import ChromeSettings
from .inputs import Inputs
import random
import time
from selenium.webdriver.common.by import By





class FirstWebPage():
    
    def __init__(self,chromesettings:ChromeSettings,inputs_instance:Inputs):
        
        self.chromesettings = chromesettings
        self.inputs_instance = inputs_instance
        self.jobtitle_firstwp = None
        self.joblocation_firstwp = None
        self.what = None
        self.where = None
        
        
    def webpage_interaction_firstwp(self):
        
        
        """Interacts with the first webpage."""
        
        

        self.jobtitle_firstwp = random.choice(self.inputs_instance.jobtitle_list)
        self.what = self.chromesettings.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/form/div[1]/div[1]/span/input",
        )
        time.sleep(self.chromesettings.random_time)
        self.what.send_keys(self.jobtitle_firstwp)

        self.joblocation_firstwp = random.choice(self.inputs_instance.joblocation_list)
        self.where = self.chromesettings.driver.find_element(
            By.XPATH,
            "/html/body/div[1]/div/form/div[1]/div[2]/span/input",
        )
        time.sleep(self.chromesettings.random_time)
        self.where.send_keys(self.joblocation_firstwp)
        

        search_jobs = self.chromesettings.driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary.btn-search")
        time.sleep(self.chromesettings.random_time)
        search_jobs.click()
        
        self.chromesettings.driver.refresh()
        
   
        time.sleep(10)
        last_week = self.chromesettings.driver.find_element(By.XPATH,"/html/body/div[1]/div[4]/div/div[3]/aside/div[2]/div/div[6]/div[2]/div/select/option[4]")
        last_week.click()
        
        
    
  

        