import os 
import pathlib
import bpy
import git
import shutil

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathBlend = os.path.join(runDir, 'Beleuchtung/Lampen/blender')
pathGLB = os.path.join(runDir, 'GLBFiles/Beleuchtung/Lampen')
os.makedirs(pathGLB, exist_ok=True)

for blendfile in os.listdir(pathBlend):
      currentFile = os.path.join(pathBlend,blendfile)
      bpy.ops.wm.open_mainfile(filepath=currentFile)
      blendfileName = blendfile.replace('.blend', '.glb')
      exportPath = os.path.join(pathGLB,blendfileName)
      bpy.ops.export_scene.gltf(export_format='GLB', filepath=exportPath, export_image_format='AUTO', convert_lighting_mode='SPEC', draco_mesh_compression_enable=False)

textureFolder = os.path.join(runDir,'Beleuchtung/Lampen/textures')
dest = os.path.join(pathGLB,'textures/')
os.makedirs(dest, exist_ok=True)
for file in os.listdir(textureFolder):
    fileDir = os.path.join(textureFolder,file)
    shutil.copy2(fileDir, dest)