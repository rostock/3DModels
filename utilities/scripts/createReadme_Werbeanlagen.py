import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Werbeanlagen')
listOfModels = os.listdir(pathThumb)
models ='## Modelle \n | Modellname | Preview | 3D-Modell | \n | --- | --- | --- |\n'
for item in listOfModels:
    image = os.path.join("../Thumbnails/Werbeanlagen",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| [Link zu Online 3D Viewer](https://3dviewer.net/embed.html#model=https://github.com/rostock/3DModels/blob/dev/GLBFiles/Werbeanlagen/"+item+".glb$camera=0,0,0$cameramode=perspective$envsettings=fishermans_bastion,on$backgroundcolor=200,200,200,255$defaultcolor=200,200,200$edgesettings=off,0,0,0,20)  |\n"
    models += string

text = """# Werbeanlagen
## Allgemein
Dieses Verzeichnis enthält Modelle von Werbetafeln und Litfaßsäulen.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Werbeanlagen/readme_Werbeanlagen.md', mode='w', encoding="utf-8") as f:
    f.write(text)
