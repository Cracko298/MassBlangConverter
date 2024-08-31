import os
from mc3dsblang import *

id = ".\\in"
od = ".\\out"

os.makedirs(id,exist_ok=True)
os.makedirs(od,exist_ok=True)

for filename in os.listdir(id):
    if filename.endswith(".json") and '-pocket' in filename:
        print(filename)
        inputFile = os.path.join(id, filename)
        with open(inputFile, "r", encoding="utf-8") as f:
            jsonData = f.read()
        
        blangFile = BlangFile().importFromJson(jsonData)
        blangFile.export(f"{od}\\{filename.replace('.json','.blang')}")

if os.name == "nt":
    os.system("pause")
