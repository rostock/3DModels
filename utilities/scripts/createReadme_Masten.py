import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Masten')
listOfModels = os.listdir(pathThumb)
listOfModels.sort()
models ='## Modelle \n | Modellname | Preview | \n | --- | --- | \n'
for item in listOfModels:
    image = os.path.join("../../Thumbnails/Masten",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| \n"
    models += string

text = """# Masten
Dieses Verzeichnis enthält Modelle von Masten. Die nachgestellte Zahl im Dateinamen entspricht dabei der Höhe des Mastes in Millimeter.

Zugehörige Lampen und Ausleger können über den Dateinamen identifiziert werden.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Beleuchtung/Masten/readme_Masten.md', mode='w', encoding="utf-8") as f:
    f.write(text)
