# Python program to explain os.mkdir() method  
      
# importing os module  
import os 
import pathlib
import shutil

runDir = pathlib.Path(__file__).parent.resolve()    
pathVerkehr = os.path.join(runDir, 'Verkehrszeichen')


for filename in os.listdir(pathVerkehr):
      if filename.endswith('.obj'):
            #print (filename)
            folder = filename.replace('rohling_', '')
            folder = folder.replace('.obj', '')
            path = os.path.join(runDir, 'Verkehrszeichen')
            path = os.path.join(path, 'textures')
            path = os.path.join(path, folder)
            for texturefile in os.listdir(path):
                  if texturefile != 'rohling.jpg':
                        #print (texturefile)
                        
                        dstObj = texturefile.replace('.jpg','.obj')
                        #print (dstObj)
                        dstMtl = texturefile.replace('.jpg','.mtl')
                        #print (dstMtl)
                        mtlFile = filename.replace('.obj','.mtl')
                        #print(mtlFile)
                        tmpFolder = os.path.join(runDir,'tmp')
                        print(tmpFolder)
                        
                        isExist = os.path.exists(tmpFolder)
                        print(isExist)
                        if isExist != True:
                              os.mkdir(tmpFolder) 
                        #print("Directory '% s' created" % path) 
                        srcObj = os.path.join(pathVerkehr,filename)
                        print(srcObj)
                        srcMtl = os.path.join(pathVerkehr,mtlFile)
                        print(srcMtl)
                        shutil.copy2(srcObj, os.path.join(tmpFolder,dstObj))
                        shutil.copy2(srcMtl, os.path.join(tmpFolder,dstMtl))
                        
for filename in os.listdir(os.path.join(runDir,'tmp')):
      if filename.endswith('.obj'):
            print (filename)                        
            
