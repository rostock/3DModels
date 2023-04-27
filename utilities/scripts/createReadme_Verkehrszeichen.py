import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Verkehrszeichen')
listOfModels = os.listdir(pathThumb)
models ='## Modelle \n | Modellname | Preview | \n | --- | --- | \n'
for item in listOfModels:
    image = os.path.join("../Thumbnails/Verkehrszeichen",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| \n"
    models += string

text = """# Verkehrszeichen
Dieses Verzeichnis enthält Modelle von Verkehrszeichen.

Die Modelle entsprechen der Größe 2. 
Es handelt sich jeweilig um einseitige Verkehrszeichen ohne Montierung und Halterungen.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen die Liste und die Abbildungen des Bundesamtes für Straßenwesen.
(https://www.bast.de/DE/Verkehrstechnik/Fachthemen/v1-verkehrszeichen/vz-start.html?nn=1817946) \n"""

text = text + models
text = text.replace("\\","/")

with open('Verkehrszeichen/readme_Verkehrszeichen.md', mode='w', encoding="utf-8") as f:
    f.write(text)