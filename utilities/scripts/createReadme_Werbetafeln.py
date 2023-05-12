import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Werbetafeln')
listOfModels = os.listdir(pathThumb)
models ='## Modelle \n | Modellname | Preview | 3D-Modell | \n | --- | --- | --- | \n'
for item in listOfModels:
    image = os.path.join("../Thumbnails/Werbetafeln",item)
    glb = os.path.join("../GBLFiles/Werbetafeln",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| https://3dviewer.net/embed.html#model=https://github.com/rostock/3DModels/blob/dev/GLBFiles/Werbetafeln/"+glb+"$camera=0,0,0$cameramode=perspective$envsettings=fishermans_bastion,on$backgroundcolor=200,200,200,255$defaultcolor=200,200,200$edgesettings=off,0,0,0,20 | \n"
    models += string

text = """# Lampen
## Allgemein
Dieses Verzeichnis enthält Modelle von Werbetafeln.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Werbetafeln/readme_Werbetafeln.md', mode='w', encoding="utf-8") as f:
    f.write(text)