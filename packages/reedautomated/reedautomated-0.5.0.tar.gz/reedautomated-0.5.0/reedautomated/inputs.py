import random

class Inputs:
    
    """Collects the data essential for the website interraction"""
    
    
    def __init__(self):
        
        self.email = None
        self.password = None
        self.job_title = None
        self.job_location = None 
        self.jobtitle_list = []
        self.joblocation_list = []
        
        
    def input_collection(self):
        
        """Collects data recquired for the program to work."""
       

        self.email = input("Please enter your Reed email: ")
        self.password = input("Please enter your Reed password: ")
        
  
        print("Up to 5 desired job titles and locations.\nIt is HIGHLY RECOMMENDED to be specific with the job title ex:'IT Support Specialist'")
            
        self.job_title = input("Enter desired job title: ")
        self.jobtitle_list.append(self.job_title)
        
        while True:
            
            job_titles_amount = input("Would you like to add an additional job title? Yes/No: ")
            
            if job_titles_amount == "Yes":
                self.job_title = input("Enter desired job title: ")
                self.jobtitle_list.append(self.job_title)
            elif job_titles_amount == "No":
                break
            else:
                print("Invalid input")
            
      
            
        self.job_location = input("Enter desired job location: ")
        self.joblocation_list.append(self.job_location)
        
        
        while True:
            
            job_locations_amount = input("Would you like to add an additional location? Yes/No: ")
            
            if job_locations_amount == "Yes":
                self.job_location = input("Enter desired job location: ")
                self.joblocation_list.append(self.job_location)
            elif job_locations_amount == "No":
                break
            else:
                print("Invalid input")
        
    
        print (f"job title list {self.jobtitle_list}\nJob location list {self.joblocation_list}")
        


           
        
    
    
    
    