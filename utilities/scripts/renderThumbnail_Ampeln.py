import bpy
import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")
# path to blendfiles   
pathBlend = os.path.join(runDir, 'Ampeln/blender')

for blendfile in os.listdir(pathBlend):
    currentFile = os.path.join(pathBlend,blendfile)
    # open the .blend file
    bpy.ops.wm.open_mainfile(filepath=currentFile)
    # create name for the image
    blendfileName = blendfile.replace('.blend', '.jpg')
    blendfileName = blendfileName.replace(" ","_")
    # create export path
    exportPath = os.path.join(runDir, 'Thumbnails/Ampeln')
    exportPathPlusName = os.path.join(exportPath,blendfileName)
    # set export format to jpeg
    bpy.context.scene.render.image_settings.file_format='JPEG'
    # set render export path
    bpy.context.scene.render.filepath = exportPathPlusName
    # set render engine to "Cycles"
    bpy.data.scenes["Scene"].render.engine = 'CYCLES'
    # set render samples
    bpy.data.scenes["Scene"].cycles.samples = 64
    # set render resolution
    bpy.data.scenes["Scene"].render.resolution_x=250
    bpy.data.scenes["Scene"].render.resolution_y=250
     # render
    bpy.ops.render.render(use_viewport = True, write_still=True)