import bpy
import os 
import pathlib


runDir = pathlib.Path(__file__).parent.resolve()
# path to blendfiles   
pathBlend = os.path.join(runDir, 'Beleuchtung/Lampen/blender')

for blendfile in os.listdir(pathBlend):
    currentFile = os.path.join(pathBlend,blendfile)
    # open the .blend file
    bpy.ops.wm.open_mainfile(filepath=currentFile)
    # create name for the image
    blendfileName = blendfile.replace('.blend', '.jpg')
    # create export path
    exportPath = os.path.join(runDir, 'Thumbnails/Lampen')
    exportPathPlusName = os.path.join(exportPath,blendfileName)
    # set export format to jpeg
    bpy.context.scene.render.image_settings.file_format='JPEG'
    # set render export path
    bpy.context.scene.render.filepath = exportPathPlusName
    # set render engine to "Cycles"
    bpy.data.scenes["Scene"].render.engine = 'CYCLES'
    # set render samples to 512
    bpy.data.scenes["Scene"].cycles.samples = 512
     # render
    bpy.ops.render.render(use_viewport = True, write_still=True)