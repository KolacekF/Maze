import os
import main

currentSize = [] #size of current maze (will be used when logging JSON size)
script_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
jsonObject = None


def OverrideMethod(x):
    global jsonObject
    
    if x == 1:
        main.ExportNiceTable = LogJson
        jsonObject = JSONobj()
    elif x == 2:
        main.ExportNiceTable = ExportText
    else:
        print("Error: method was not overriden")

#method that override
def ExportText(PrintTable):
    name = "export.txt"
    
    with open(os.path.join(script_dir, name), "a", encoding="utf-8") as f:
        for line in PrintTable:
            printLine = ""
            for char in line:
                printLine += char
            f.write(printLine)
            f.write("\n")
        f.write("\n")

    print(f"{name} was succesfully saved")

#method that override
def LogJson(PrintTable):
    sizeStr = f"size{currentSize[0]}x{currentSize[1]}"
    jsonObject.setData(sizeStr, PrintTable)

def ExportJSON():
    name = "export.json"
    
    with open(os.path.join(script_dir, name), "w", encoding="utf-8") as f:
        f.write(jsonObject.getData())

    print(f"{name} was succesfully saved")

class JSONobj:
    def __init__(self):
        self.json = {
           "data": {}
        }
    def setData(self, size, data):
        if size not in self.json["data"].keys():
           self.json["data"][size] = []
        self.json["data"][size].append(data)
    def getData(self):
        import json
        return json.dumps(self.json, indent=4)

if __name__ == "__main__":
    #for which sizes will hte mazes be made
    sizes = [[3, 3], [5, 5], [10,10], [20, 10], [30, 5], [40, 5]]
    #if true, JSON is created, in default TXT will be created
    createJson = True
    
    if createJson:
        OverrideMethod(1) #creates JSON
    else: 
        OverrideMethod(2) #creates and saves TXT

    for size in sizes:
        currentSize = size
        main.Run(size, 0)

    if createJson:
        ExportJSON() #saves JSON