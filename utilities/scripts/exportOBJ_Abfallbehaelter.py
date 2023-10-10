import os 
import pathlib
import bpy
import git
import shutil

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathBlend = os.path.join(runDir, 'Abfallbehaelter/blender')
pathOBJ = os.path.join(runDir, 'ObjectFiles/Abfallbehaelter')
os.makedirs(pathOBJ, exist_ok=True)

for blendfile in os.listdir(pathBlend):
      currentFile = os.path.join(pathBlend,blendfile)
      bpy.ops.wm.open_mainfile(filepath=currentFile)
      blendfileName = blendfile.replace('.blend', '.obj')
      exportPath = os.path.join(pathOBJ,blendfileName)
      bpy.ops.export_scene.obj(filepath=exportPath, axis_forward='-Y', axis_up='Z', use_materials=True, path_mode='RELATIVE')

textureFolder = os.path.join(runDir,'Abfallbehaelter/textures')
dest = os.path.join(pathOBJ,'textures/')
os.makedirs(dest, exist_ok=True)
for file in os.listdir(textureFolder):
    fileDir = os.path.join(textureFolder,file)
    shutil.copy2(fileDir, dest)

# replace texture reference in .mtl                     
for filename in os.listdir(pathOBJ):
      if filename.endswith('.mtl'):
            #read mtl file
            fin = open(os.path.join(pathOBJ, filename), "rt")
            #read file contents to string
            data = fin.read()
            #replace all occurrences of the required string
            data = data.replace('../../','../')
            #close the input file
            fin.close()
            #open the input file in write mode
            fin = open(os.path.join(pathOBJ, filename), "wt")
            #overrite the input file with the resulting data
            fin.write(data)
            #close the file
            fin.close()