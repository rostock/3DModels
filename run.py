# Python program to explain os.mkdir() method  
      
# importing os module  
import os 
import pathlib
    
# Directory 
directory = "models"
runDir = pathlib.Path(__file__).parent.resolve()    
# Path 
path = os.path.join(runDir, directory)  

os.mkdir(path) 
print("Directory '% s' created" % directory) 
