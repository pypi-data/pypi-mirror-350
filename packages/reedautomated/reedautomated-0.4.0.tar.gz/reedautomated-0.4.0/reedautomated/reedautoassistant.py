from .inputs import Inputs
from .chromesettings import ChromeSettings
from .firstwebpage import FirstWebPage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException
import time 
import random



class AutoAssistant():
    
    
    def __init__(self, chromesettings:ChromeSettings,inputs_instance:Inputs,firstwp:FirstWebPage):
        
        self.chromesettings = chromesettings
        self.inputs_instance = inputs_instance
        self.firstwp = firstwp
        self.job_spec_name = None
        self.location_spec_name = None
        self.job_location_text = None
        self.job_title_text = None
        self.job_card_bodies = None
        self.job_card_body = None
        self.jobbody_amount = True
       
       



    def job_selection(self):
        
        """Finds the jobs from the website."""
        
        
        what_jobprocess = self.chromesettings.driver.find_element(By.CSS_SELECTOR, 'input[data-qa="searchKeywordInput"]')
        where_jobprocess = self.chromesettings.driver.find_element(By.CSS_SELECTOR, 'input[data-qa="searchLocationInput"]')
        
        what_value = what_jobprocess.get_attribute("value")
        where_value = where_jobprocess.get_attribute("value")
        

        self.job_spec_name = what_value
        self.location_spec_name = where_value
            
                 
        print(f'what_value={what_value}, where_value={where_value}')
        print(f'what_from_page={self.job_spec_name}, where_from_page={ self.location_spec_name}')
        
        time.sleep(10)
        self.job_card_bodies = self.chromesettings.driver.find_elements(By.CSS_SELECTOR, "div.job-card_jobCard__body__86jgk.card-body")
        
        while self.jobbody_amount:

            if len(self.job_card_bodies) < 3:
                self.jobbody_amount = False
                self.chromesettings.driver.close()
            
            else:
                for self.job_card_body in self.job_card_bodies:
                    
                    
                    job_location = self.job_card_body.find_element(By.CSS_SELECTOR, "li[data-qa='job-card-location']")
                    job_title = self.job_card_body.find_element(By.CSS_SELECTOR, "[data-qa='job-card-title']")
            
                    self.job_location_text = job_location.text
                    self.job_title_text = job_title.text
                    
                    
                    print(
                                f"Current value in the ITERATION = {self.job_spec_name} and  {self.location_spec_name} \nWeb element names {self.job_title_text} and {self.job_location_text}"
                            )
                
                    if  self.job_spec_name.lower() in self.job_title_text.lower() and self.location_spec_name.lower() in self.job_location_text.lower():
                        print(f'JOB NAME SELECTED: {self.job_spec_name} \nLOCATION NAME SELECTED: {self.location_spec_name}')
                        

                        try:
                            index_job_card = self.job_card_bodies.index(self.job_card_body)
                            print(f'this is the current amount of card bodies: {len(self.job_card_bodies)}')
                            
                            self.chromesettings.driver.execute_script("arguments[0].scrollIntoView(true);", self.job_card_body)

                            try:
                                main_job_card = self.job_card_body.find_element(By.CSS_SELECTOR, 'button[data-qa="applyJobBtn"]')
                            
                            except Exception as e:
                                print(f'No main job card {e}\n Trying to find the job suggestion')
                                try:
                                    unshortlist = self.job_card_body.find_element(By.CSS_SELECTOR, "button[aria-label='Unshortlist job']")   
                                    print(f"unshort list button already been clicked.")
                                except NoSuchElementException:      
                                    job_suggestion = self.job_card_body.find_element(By.CSS_SELECTOR, "button.job-card_btnShortlistJob__jgO8k.btn.btn-inline")
                                    
                                    self.chromesettings.driver.execute_script("arguments[0].click();", job_suggestion)
                                    self.job_card_bodies.pop(index_job_card)
                                    print('Your job suggestion found')

                            main_jobcard_active = self.job_card_body.find_element(By.CSS_SELECTOR, "button.job-card_applyBtn__2N2jy.btn.btn-secondary:not(.disabled)")
                            time.sleep(self.chromesettings.random_time)
                            self.chromesettings.driver.execute_script("arguments[0].click();", main_jobcard_active)
                            print("MAIN ACTIVE CLICKED")
                            
                            job_description = self.chromesettings.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-qa='submit-application-btn']")))
                            time.sleep(self.chromesettings.random_time)
                            job_description.click()
                            
                            try:
                                ok_button = self.chromesettings.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.application-confirmation-modal_continueButton__i73Dl.btn.btn-primary')))
                                time.sleep(self.chromesettings.random_time)
                                ok_button.click()
                            
                            except Exception as e:
                                print(f'OK button exception: {e}')
                                x_button = self.chromesettings.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div > div.modal.overflow-auto.fade.show.d-block > div > div > header > button')))
                                x_button.click()

                                self.job_card_bodies.pop(index_job_card)
                                print(f'index of the job card {self.job_card_bodies.index(self.job_card_body)} successfully removed')
                        except Exception as e:
                                print(f'Main job card NOT FOUND: {e}')
                
                # Else condition
                try:
                    
                    next_page_button = self.chromesettings.driver.find_element(By.CSS_SELECTOR, "a.page-link.next[aria-label='Next page']")
                    self.chromesettings.driver.execute_script("arguments[0].click();", next_page_button)
                    
                    return self.job_selection()
                
                except Exception as e:
                    print(f'Next page button exception: {e}')
                    # return False

            