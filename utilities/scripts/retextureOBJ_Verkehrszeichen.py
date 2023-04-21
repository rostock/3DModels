# Python program to explain os.mkdir() method  
      
# importing os module  
import os 
import pathlib
import shutil
import git

runDir = git.Repo(".",search_parent_directories=True)
runDir = runDir.git.rev_parse("--show-toplevel") 
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen/tmp')

pathOBJ = os.path.join(runDir, 'ObjectFiles/Verkehrszeichen')
os.makedirs(pathOBJ, exist_ok=True)

texturesFolder = os.path.join(pathOBJ,'textures/')
os.makedirs(texturesFolder, exist_ok=True)

for filename in os.listdir(pathVerkehr):
      if filename.endswith('.obj'):
            folder = filename.replace('.obj', '')
            # Create Texture Subfolder
            typeFolder = os.path.join(texturesFolder,folder)
            os.mkdir(typeFolder)
            path = os.path.join(runDir, 'Verkehrszeichen')
            path = os.path.join(path, 'textures')
            path = os.path.join(path, folder)
            for texturefile in os.listdir(path):
                  if texturefile != 'rohling.jpg':
                        dstObj = texturefile.replace('.jpg','.obj')
                        dstMtl = texturefile.replace('.jpg','.mtl')
                        mtlFile = filename.replace('.obj','.mtl')
                        print(texturefile)
                        srcObj = os.path.join(pathVerkehr,filename)
                        print(srcObj)
                        srcMtl = os.path.join(pathVerkehr,mtlFile)
                        print(srcMtl)
                        srcJPG = os.path.join(path,texturefile)
                        print(srcJPG)
                        shutil.copy2(srcObj, os.path.join(pathOBJ,dstObj))
                        shutil.copy2(srcMtl, os.path.join(pathOBJ,dstMtl))
                        shutil.copy2(srcJPG, os.path.join(typeFolder,texturefile))
            
            #replace mtl reference in .obj
            pathOBJ = os.path.join(runDir, 'ObjectFiles/Verkehrszeichen')
            oldText = filename.replace('obj','mtl')
            print("MTL reference to replace: "+ oldText)
            for obj in os.listdir(pathOBJ):
                  if obj.endswith('.obj'):
                        newText = obj.replace('obj','mtl')
                        print (obj)  
                        print ("MTL replacement: "+ newText)  
                        #read obj file
                        fin = open(os.path.join(pathOBJ, obj), "rt")
                        #read file contents to string
                        data = fin.read()
                        #replace all occurrences of the required string
                        data = data.replace(oldText, newText)
                        #close the input file
                        fin.close()
                        #open the input file in write mode
                        fin = open(os.path.join(pathOBJ, obj), "wt")
                        #overrite the input file with the resulting data
                        fin.write(data)
                        #close the file
                        fin.close()

                        
# replace texture reference in .mtl                     
pathOBJ = os.path.join(runDir, 'ObjectFiles/Verkehrszeichen')
oldText = "rohling.jpg"
for filename in os.listdir(pathOBJ):
      if filename.endswith('.mtl'):
            newText = filename.replace('mtl','jpg')  
            #read mtl file
            fin = open(os.path.join(pathOBJ, filename), "rt")
            #read file contents to string
            data = fin.read()
            #replace all occurrences of the required string
            data = data.replace(oldText, newText)

            data = data.replace('..\\\\',' ')
            #close the input file
            fin.close()
            #open the input file in write mode
            fin = open(os.path.join(pathOBJ, filename), "wt")
            #overrite the input file with the resulting data
            fin.write(data)
            #close the file
            fin.close()

# delete template files from 'pathVerkehr'
shutil.rmtree(pathVerkehr)


            
            
            
