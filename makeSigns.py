import os 
import pathlib
import shutil

runDir = pathlib.Path(__file__).parent.resolve()    
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')

for filename in os.listdir(pathVerkehr):
    newname = filename + "new"
    if filename.endswith('.obj'):
      shutil.copy(filename, "as", newname
