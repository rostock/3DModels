import os 
import pathlib
import shutil

runDir = pathlib.Path(__file__).parent.resolve()
pathVerkehr = os.path.join(runDir, 'OBJ')

for filename in os.listdir(pathVerkehr):
    if filename.endswith('.obj'):
        base, extension = os.path.splitext(filename)
        oldname = str(pathVerkehr) + "\\" + filename
        newname = str(pathVerkehr) + "\\" + base + "_new" + extension
        print(oldname)
        print(newname)
        shutil.copy(oldname, newname)
