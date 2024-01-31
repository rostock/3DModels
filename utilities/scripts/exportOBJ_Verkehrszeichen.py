import os 
import pathlib
import bpy
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')
pathTemp = os.path.join(pathVerkehr, 'tmp')
os.makedirs(pathTemp, exist_ok=True)
blendPath = os.path.join(pathVerkehr, 'blender')
for blendfile in os.listdir(blendPath):
      currentFile = os.path.join(blendPath,blendfile)
      bpy.ops.wm.open_mainfile(filepath=currentFile)
      blendfileName = blendfile.replace('.blend', '.obj')
      exportPath = os.path.join(pathTemp,blendfileName)
      bpy.ops.wm.obj_export(filepath=exportPath, forward_axis='NEGATIVE_Y', up_axis='Z', export_materials=True, export_triangulated_mesh=True, path_mode='RELATIVE')