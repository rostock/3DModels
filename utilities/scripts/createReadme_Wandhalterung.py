import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Wandhalterung')
listOfModels = os.listdir(pathThumb)
listOfModels.sort()
models ='## Modelle \n | Modellname | Preview | \n | --- | --- | \n'
for item in listOfModels:
    image = os.path.join("../../Thumbnails/Wandhalterung",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| \n"
    models += string

text = """# Wandhalterung
Dieses Verzeichnis enthält Modelle von Wandhalterungen. Die nachgestellten Parameter beschreiben Offsets der zugehörigen Lampe relativ zur Hauptachse des Mastes in Millimeter.

Zugehörige Lampen können über den Dateinamen identifiziert werden.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Beleuchtung/Wandhalterung/readme_Wandhalterung.md', mode='w', encoding="utf-8") as f:
    f.write(text)
