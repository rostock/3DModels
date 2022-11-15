import os 
import pathlib
import bpy

runDir = pathlib.Path(__file__).parent.resolve()    
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')

blendPath = os.path.join(pathVerkehr, 'blender')
for blendfile in os.listdir(blendPath):
      currentFile = os.path.join(blendPath,blendfile)
      bpy.ops.wm.open_mainfile(filepath=currentFile)
      blendfileName = blendfile.replace('.blend', '.obj')
      exportPath = os.path.join(pathVerkehr,blendfileName)
      bpy.ops.export_scene.obj(filepath=exportPath, axis_forward='-Y', axis_up='Z', use_materials=True)