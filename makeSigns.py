import os 
import pathlib
import shutil

runDir = pathlib.Path(__file__).parent.resolve()
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')

for filename in os.listdir(pathVerkehr):
    if filename.endswith('.obj'):
        # Directory
        directory = "obj_files"
  
        # Parent Directory path
        parent_dir = runDir
        # Path
        path = os.path.join(parent_dir, directory)
        # mkdir
        os.mkdir(path)
        
        base, extension = os.path.splitext(filename)
        oldname = str(pathVerkehr) + "/" + filename
        newname = str(path) + "/" + base + "_new" + extension
        print(oldname)
        print(newname)
        shutil.copy(oldname, newname)
