import os 
import pathlib
import bpy
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")
temp = os.path.join(runDir, 'ObjectFiles/Verkehrszeichen')

for obj in os.listdir(temp):
    if obj.endswith(".obj"):
        # default blendfile to import .obj into
        blendFile =  os.path.join(runDir,"utilities/default.blend")
        # obj file
        objPath = os.path.join(temp, obj)
        # open .blend
        bpy.ops.wm.open_mainfile(filepath=blendFile)
        # import .obj
        #bpy.ops.wm.obj_import(filepath=objPath, forward_axis="Y")
        bpy.ops.import_scene.obj(filepath=objPath, axis_forward="Y")
        # create name for the image
        name = obj.replace('.obj', '.jpg')
        # create export path
        exportPath = os.path.join(runDir, 'Thumbnails/Verkehrszeichen')
        exportPathPlusName = os.path.join(exportPath,name)
        # align camera to selected
        bpy.ops.view3d.camera_to_view_selected()
        # zoom out slightly
        bpy.data.cameras['Camera'].lens=100
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
    else:
        pass
