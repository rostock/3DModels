# Python program to explain os.mkdir() method  
      
# importing os module  
import os 
import pathlib
import shutil

runDir = pathlib.Path(__file__).parent.resolve()    
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')

tmpFolder = os.path.join(runDir,'tmp')
os.mkdir(tmpFolder) 
texturesFolder = os.path.join(tmpFolder,'textures')
os.mkdir(texturesFolder)

for filename in os.listdir(pathVerkehr):
      if filename.endswith('.obj'):
            #folder = filename.replace('rohling_', '')
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
                        shutil.copy2(srcObj, os.path.join(tmpFolder,dstObj))
                        shutil.copy2(srcMtl, os.path.join(tmpFolder,dstMtl))
                        shutil.copy2(srcJPG, os.path.join(typeFolder,texturefile))
            
            #replace mtl reference in .obj
            tmpPath = os.path.join(runDir,'tmp')
            oldText = filename.replace('obj','mtl')
            print("MTL reference to replace: "+ oldText)
            for obj in os.listdir(tmpPath):
                  if obj.endswith('.obj'):
                        newText = obj.replace('obj','mtl')
                        print (obj)  
                        print ("MTL replacement: "+ newText)  
                        #read obj file
                        fin = open(os.path.join(tmpPath, obj), "rt")
                        #read file contents to string
                        data = fin.read()
                        #replace all occurrences of the required string
                        data = data.replace(oldText, newText)
                        #close the input file
                        fin.close()
                        #open the input file in write mode
                        fin = open(os.path.join(tmpPath, obj), "wt")
                        #overrite the input file with the resulting data
                        fin.write(data)
                        #close the file
                        fin.close()

                        
# replace texture reference in .mtl                     
tmpPath = os.path.join(runDir,'tmp')
oldText = "rohling.jpg"
for filename in os.listdir(tmpPath):
      if filename.endswith('.mtl'):
            newText = filename.replace('mtl','jpg')  
            #read mtl file
            fin = open(os.path.join(tmpPath, filename), "rt")
            #read file contents to string
            data = fin.read()
            #replace all occurrences of the required string
            data = data.replace(oldText, newText)
            #close the input file
            fin.close()
            #open the input file in write mode
            fin = open(os.path.join(tmpPath, filename), "wt")
            #overrite the input file with the resulting data
            fin.write(data)
            #close the file
            fin.close()


            
            
            
