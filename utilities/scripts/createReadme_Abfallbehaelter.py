import os 
import pathlib
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel")     
pathThumb = os.path.join(runDir, 'Thumbnails/Abfallbehaelter')
listOfModels = os.listdir(pathThumb)
models ='## Modelle \n | Modellname | Preview | \n | --- | --- | \n'
for item in listOfModels:
    image = os.path.join("../../Thumbnails/Abfallbehaelter",item)
    item = item.replace('.jpg','')
    string = "| "+item+" |![Image]("+image +")| \n"
    models += string

text = """# Abfallbehaelter
Dieses Verzeichnis enthält Modelle von Abfallbehaeltern, welche in der Hansestadt Rostock im öffentlichen Raum aufgestellt sind.

## Grundlage
Als Grundlage für die zur Verfügung gestellten Modelle dienen **Fotos** und **Produktskizzen/-maße** der jeweiligen Realweltobjekte. \n"""

text = text + models
text = text.replace("\\","/")

with open('Abfallbehaelter/readme_Abfallbehaelter.md', mode='w', encoding="utf-8") as f:
    f.write(text)