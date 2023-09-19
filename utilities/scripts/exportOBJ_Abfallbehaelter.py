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