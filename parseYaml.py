import  yaml
import os
folder = 'E:\\games\\Steam\\steamapps\\common\\Empyrion - Galactic Survival'
for root, dirs, files in os.walk(folder):
    #path = root.split(os.sep)
    #print((len(path) - 1) * '---', os.path.basename(root))
    for file in files:
        if file.lower() == 'sectors.yaml' :
           print(root, file)
           with open(root+'\\'+file, 'rb')  as fileHandle :
               string = fileHandle.read()
           string = string.replace(b"\t", b"")
           obj = yaml.load(string)
           if type(obj).__name__ == 'list' :
               planets = obj
           else:
               planets = obj['Sectors']
           print( len(planets), 'planets')
