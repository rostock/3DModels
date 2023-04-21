import os 
import pathlib
import git

preText = "# Inhalt \n"
preText += """Dieses Repository enthält .OBJ Modelle für:
- [Beleuchtung](#Beleuchtung)
    - [Lampen](#Lampen)
    - [Ausleger](#Ausleger)
    - [Masten](#Masten)
- Verkehrszeichen\n
"""

preText += "# Beleuchtung \n"
text = ''
with open('Beleuchtung/Lampen/readme_Lampen.md', mode='r', encoding="utf-8") as data_Lampen:
    text += data_Lampen.read()+"\n"
with open('Beleuchtung/Ausleger/readme_Ausleger.md', mode='r', encoding="utf-8") as data_Ausleger:
    text += data_Ausleger.read()+"\n"
with open('Beleuchtung/Masten/readme_Masten.md', mode='r', encoding="utf-8") as data_Masten:
    text += data_Masten.read()+"\n"
 
text = text.replace('# ','## ')
text = text.replace('../../','')

preText += text


fullText = preText




with open('readme.md', mode='w', encoding="utf-8") as f:
    f.write(fullText)