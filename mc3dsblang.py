import os
import json
from pathlib import Path

class MC3DSBlangException(Exception):
    def __init__(self, message):
        super().__init__(message)

class BlangFile:
    def __init__(self):
        return
    
    def open(self, path: str|Path):
        if isinstance(path, str):
            path = Path(path)
        elif isinstance(path, Path):
            pass
        else:
            raise TypeError("path must be a 'str' or 'Path'")
        
        with open(path, "rb") as f:
            file_content = list(f.read())

        # Obtener longitud
        long = []
        for i in range(0, 4):
            long.append(file_content[i])
        long = int.from_bytes(bytearray(long), "little")

        # Obtener los elementos del indice
        idx = 4
        data = []
        for i in range(0, long):
            join = []
            for j in range(0, 4):
                join.append(file_content[idx])
                idx += 1
            data.append(join)
            idx += 4

        # Longitud de los textos
        textlong = []
        for i in range(idx, idx + 4):
            textlong.append(file_content[i])
        textlong = int.from_bytes(bytearray(textlong), "little")

        # Obtener los textos
        idx += 4
        texts = []
        for i in range(0, long):
            join = []
            while file_content[idx] != 0:
                join.append(file_content[idx])
                idx += 1
            texts.append(bytearray(join).decode("utf-8"))
            idx += 1

        self.data = data
        self.texts = texts
        return self
    
    def getData(self):
        return self.data

    def getTexts(self) -> list:
        return self.texts

    def replace(self, idx: int, newtext: str):
        if type(idx) != int:
            raise MC3DSBlangException("idx must be an 'int'")
        if type(newtext) != str:
            raise MC3DSBlangException("newtext must be a 'str'")

        if idx >= 0 and idx < len(self.texts):
            if newtext != "" and newtext != '':
                self.texts[idx] = newtext
            else:
                self.texts[idx] = " "
        return
    
    def export(self, path: str):
        if type(path) != str:
            raise MC3DSBlangException("path must be a 'str'")

        long = len(self.data)
        indexLong = list(long.to_bytes(4, "little"))

        indexData = []
        textData = []
        for i in range(0, long):
            # Copiar los primeros datos del elemento
            indexData.extend(self.data[i])

            # Posición de texto
            indexData.extend(list(len(textData).to_bytes(4, "little")))
            
            # Agregar texto
            textData.extend(list(self.texts[i].encode("utf-8")))

            # Separador/terminador
            textData.append(0)

        textsLong = list(len(textData).to_bytes(4, "little"))

        # Junta todo en una sola lista
        self.exportData = []
        self.exportData.extend(indexLong)
        self.exportData.extend(indexData)
        self.exportData.extend(textsLong)
        self.exportData.extend(textData)

        self.exportData = bytearray(self.exportData)

        with open(path, "wb") as f:
            f.write(self.exportData)
        return

    def exportToJson(self, path: str):
        long = len(self.data)
        dataDictionary = {}
        for i in range(0, long):
            identifier = bytearray(self.data[i])
            identifier = int.from_bytes(identifier, "little")
            identifier = str(identifier)
            
            dataDictionary[identifier] = {}
            dataDictionary[identifier]["order"] = i + 1
            dataDictionary[identifier]["text"] = self.texts[i]
        
        outFile = open(path, "w", encoding="utf-8")
        json.dump(dataDictionary, outFile, indent=4, ensure_ascii=False)
        outFile.close()
        return
    
    def importFromJson(self, json_string: str):
        if type(json_string) != str:
            raise MC3DSBlangException("path must be a 'str'")

        data = []
        texts = []

        dataDictionary = json.loads(json_string)

        idx = 1
        while idx <= len(dataDictionary):
            for key in dataDictionary:
                if dataDictionary[key]["order"] == idx:
                    data.append(list(int(key).to_bytes(4, "little")))
                    texts.append(dataDictionary[key]["text"])
                    idx += 1
                    break

        self.data = data
        self.texts = texts
        return self