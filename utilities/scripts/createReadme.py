import os 
import pathlib
import git

text = "# 3D Modelle \n Dieses Repository enthält .OBJ Modelle für: \n"

currentCategory = ''
for path in pathlib.Path().rglob('*.md'):
    if path.name != 'readme.md':
        topic = path.name.split("_")
        topic = topic[1].split(".")
        topic = topic[0]
        if len(str(path).split("\\")) > 2:
            category = str(path).split("\\")[0]
            if currentCategory != category:
                text += "- "+ category +"\n"
                currentCategory = category
            text += "   - ["+topic+"]"+"("+str(path)+") \n"
        else:
            text += "- ["+topic+"]"+"("+str(path)+") \n"

with open('readme.md', mode='w', encoding="utf-8") as f:
   f.write(text)