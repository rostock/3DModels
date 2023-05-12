import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Werbetafeln')
listOfModels = os.listdir(pathThumb)
models ='## Modelle \n | Modellname | Preview | \n | --- | --- |\n'
for item in listOfModels:
    image = os.path.join("../Thumbnails/Werbetafeln",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| \n"
    models += string

text = """# Werbetafelnn
## Allgemein
Dieses Verzeichnis enthält Modelle von Werbetafeln.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Werbetafeln/readme_Werbetafeln.md', mode='w', encoding="utf-8") as f:
    f.write(text)
