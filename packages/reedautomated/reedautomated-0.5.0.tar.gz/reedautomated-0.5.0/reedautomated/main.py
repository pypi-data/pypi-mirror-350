from .inputs import Inputs
from .chromesettings import ChromeSettings
from .firstwebpage import FirstWebPage
from .login import Login
from .reedautoassistant import AutoAssistant
import schedule
import time
import random



class MainInteraction():
    
    def __init__(self):
        self.input_instance = Inputs()
        
      
    def job_tasks(self):
        
        """Function that contain most of the interactions with the website"""
        
    
        chrosettings = ChromeSettings()
        login = Login(chrosettings,self.input_instance)
        firstwp = FirstWebPage(chrosettings,self.input_instance)
        autoassistant = AutoAssistant(chrosettings,self.input_instance,firstwp)
        
        try:
            login.loginpage_interaction()
            firstwp.webpage_interaction_firstwp()
            autoassistant.job_selection()
        except Exception as err:
            print(f"Error at {err}")
            chrosettings.driver.close()
            
    
        
maininteraction_instance = MainInteraction()
    

def main():
    """Scheduling of the job searching"""


    schedule.every(random.choice(range(5,11))).minutes.do(maininteraction_instance.job_tasks)
    while True:
        schedule.run_pending()
        time.sleep(1)
     
     
def run_as_script():
    
    """Runs the entire main.py file as a script"""
    
    maininteraction_instance.input_instance.input_collection()
    main()




if __name__ == "__main__":
    run_as_script()
 