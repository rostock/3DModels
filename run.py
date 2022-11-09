# Python program to explain os.mkdir() method  
      
# importing os module  
import os 
import pathlib
import shutil
    
# Directory 
directory = "models"
runDir = pathlib.Path(__file__).parent.resolve()    
# Path 
path = os.path.join(runDir, directory)  

os.mkdir(path) 
print("Directory '% s' created" % path) 

for filename in os.listdir(os.path.join(runDir, 'Verkehrszeichen')):
      if filename.endswith('.obj'):
            print (filename)
            folder = filename.replace('rohling_', '')
            folder = folder.replace('.obj', '')
            path = os.listdir(runDir, 'Verkehrszeichen')
            path = os.listdir(path, 'textures')
            path = os.listdir(path, folder)
            for texturefile in os.listdir(path):
                  print (texturefile)
            
