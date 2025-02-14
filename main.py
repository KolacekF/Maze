import random
import time

Cells = [] # list [Object, Object, Object, ...]
StartingCell = None #object
FinalCell = None #object

def FindPath(): #returns True if path exists, otherwise returns False
    path = [] # list [Object, Object, Object, ...]
    pathFound = False
    pathExists = True
    for obj in Cells:
        if not obj: continue #if False at the start of the list
        obj.lastCheckedNeighbor = -1 #reset .lastCheckedNeighbor
        #print(f"reset .lastCheckedNeighbor: {obj.position.get(), obj.lastCheckedNeighbor}") #DEBUGGING

    def prevCell():
        #print(path, len(path)) #DEBUGGING
        #for x in path: #DEBUGGING
        #    if not x: continue #DEBUGGING
        #    print(x.position.get(), x.lastCheckedNeighbor) #DEBUGGING
        if(len(path) == 1): #failsafe if there is no path, then StartingCell must have been path.pop()
            pathExists = False
            return False
        if(path[-1].lastCheckedNeighbor != 3):
            #return path[-1].Path(path[-2])
            return True
        else:
            path.pop()
            return prevCell()

    path.append(False)
    path.append(StartingCell)
    #print(path) #DEBUGGING
    while( not pathFound and pathExists):
        #print(f"path: {path}") #DEBUGGING
        #for x in path: #DEBUGGING
        #    if not x: continue #DEBUGGING
        #    print(x.position.get(), x.lastCheckedNeighbor) #DEBUGGING
        result = path[-1].Path(path[-2])
        #print(f"result: {result}") #DEBUGGING

        if(result == False or result in path): #no next path, so go back || result == Object that is already on path, go back. The path cant go over itself - that will cause bugs
            #path.append(prevCell())
            if not prevCell(): pathExists = False
        else: #result == Object, so go next
            path.append(result)

        if(result == FinalCell): pathFound = True

    if( not pathExists):
        return False
    else:
        return True

def NoIsolated():
    workingList = [] #so that you can .pop() from this list and not from the main one Cells[]

    def inner(cell):
        if cell in workingList: #if cell is not in workingList (already .poped), no need to recursive calling
            workingList.remove(cell)
            for i in [0, 1, 2, 3]:
                if cell.border[i] != 1:
                    inner(cell.neighbors[i])

    for cell in Cells:
        workingList.append(cell)

    inner(StartingCell)

    return len(workingList)

def SetBorder(): #returns False if no other border can be set on all Cells{} in Cells[], returns [obj, obj] of the changed Cells{} if border was set
    workingList = [] #so that you can .pop() from this list and not from the main one Cells[]
    borderCanBeSet = True
    tempVar_result = [] #previous state of border from Cell{}

    def inner(): #sets border for random Cell{} & returns previous state of the border, returns False if no other border can be set FOR GIVEN CELL
        obj = workingList[random.randint(0, len(workingList) - 1)]
        result = obj.Border()
        return [result, obj]

    #workingList = Cells.copy()
    for cell in Cells:
        if cell.border.count(-1) > 0: workingList.append(cell)
    while(True):
        #print(f"workingList: {len(workingList)}") #DEBUGGING
        if(len(workingList) == 0): #failsafe if no border can be added
            borderCanBeSet = False
            break

        result = inner()

        if(result[0]): #if border is set
            tempVar_result = result[0].copy()
            break 
        else: #if border cannot be set, .pop() the obj (Cell{}) from workingList[]
            workingList.remove(result[1])

    if( not borderCanBeSet):
        return False
    else:
        #print(f"tempVar_result: {str(tempVar_result[0]), str(tempVar_result[1])}") #DEBUGGING
        return tempVar_result

def Show(iteration): #when called, prints() table based on data from Cells[]
    row = 0
    column = 0
    CharRow_upp = ""
    CharRow_mid = ""
    CharRow_bot = ""
    PrintTable = []
    borderChar = "*"
    StartingChar = "X"
    FinalChar = "°"
    freeBorders = 0
    
    def returnBorderChar(border):
        if(border == 1):
            return borderChar
        else:
            return " "
    def returnCellChar(cell):
        if(cell == StartingCell):
            return StartingChar
        elif(cell == FinalCell):
            return FinalChar
        else:
            return " "
    def inner(i, input):
        try:
            PrintTable[i] = input
        except IndexError:
            PrintTable.append(input)

    for cell in Cells:
        if(cell.position.y != row):
            referenceI = row * 2

            #PrintTable[referenceI] = CharRow_upp
            #PrintTable[referenceI + 1] = CharRow_mid
            #PrintTable[referenceI + 2] = CharRow_bot
            inner(referenceI, CharRow_upp)
            inner(referenceI + 1, CharRow_mid)
            inner(referenceI + 2, CharRow_bot)

            CharRow_upp = ""
            CharRow_mid = ""
            CharRow_bot = ""
            
            column = 0
            row += 1
        
        if(column == 0):
            CharRow_upp += borderChar
            CharRow_mid += returnBorderChar(cell.border[2])
            CharRow_bot += borderChar

        CharRow_upp += returnBorderChar(cell.border[1])
        CharRow_mid += returnCellChar(cell)
        CharRow_bot += returnBorderChar(cell.border[3])

        CharRow_upp += borderChar
        CharRow_mid += returnBorderChar(cell.border[0])
        CharRow_bot += borderChar

        column += 1
    referenceI = row * 2
    inner(referenceI, CharRow_upp)
    inner(referenceI + 1, CharRow_mid)
    inner(referenceI + 2, CharRow_bot)

    for cell in Cells:
        freeBorders += cell.border.count(-1)

    print(f"number of cells: {len(Cells)}, starting cell on {StartingCell.position.get()}, final cell on {FinalCell.position.get()}, iteration: {iteration}, unset borders: {freeBorders}")
#    for r in PrintTable:
#        print(r)
    for line in NiceTable(PrintTable, borderChar, StartingChar, FinalChar):
        printLine = ""
        for char in line:
            printLine += char
        print(printLine)
    #for cell in Cells: #DEBUGGING
    #    if not cell: continue #DEBUGGING
    #    print(cell.position.get(), cell.border) #DEBUGGING

def NiceTable(table, borderChar, StartingChar = " ", FinalChar = " "):
    tableX = len(table[0])
    tableY = len(table)
    PrintTable = [[" "] * tableX for x in range(tableY)]
    
    def inner(x, y):
        if x in range(tableX) and y in range(tableY):
            if table[y][x] == borderChar: return 1
        return 0
    
    def unicodeChar(neighbors): #list [-1, -1, 0, 1] - right, upper, left, bottom
        ch = ""

        if neighbors == [0, 0, 0, 0]:
            ch = " "
        elif neighbors == [1, 0, 0, 0] or neighbors == [0, 0, 1, 0] or neighbors == [1, 0, 1, 0]:
            ch = u"\u2501" #-
        elif neighbors == [0, 1, 0, 0] or neighbors == [0, 0, 0, 1] or neighbors == [0, 1, 0, 1]:
            ch = u"\u2503" #|
        elif neighbors == [1, 0, 0, 1]:
            ch = u"\u250f"
        elif neighbors == [1, 1, 0, 0]:
            ch = u"\u2517" #|_
        elif neighbors == [0, 0, 1, 1]:
            ch = u"\u2513" 
        elif neighbors == [0, 1, 1, 0]:
            ch = u"\u251b" #_|
        elif neighbors == [1, 1, 0, 1]:
            ch = u"\u2523" #|-
        elif neighbors == [1, 1, 1, 0]:
            ch = u"\u253b" 
        elif neighbors == [0, 1, 1, 1]:
            ch = u"\u252b" #-|
        elif neighbors == [1, 0, 1, 1]:
            ch = u"\u2533" 
        elif neighbors == [1, 1, 1, 1]:
            ch = u"\u254b" #cross
        else:
            ch = "E"
        
        return ch
    
    for y in range(tableY):
        for x in range(tableX):
            if table[y][x] == borderChar:
                PrintTable[y][x] = unicodeChar([inner(x+1, y), inner(x, y-1), inner(x-1, y), inner(x, y+1)])
            elif table[y][x] == StartingChar:
                PrintTable[y][x] = StartingChar
            elif table[y][x] == FinalChar:
                PrintTable[y][x] = FinalChar
            #print(y, x, PrintTable) #DEBUGGING
    #import json                                        #DELETE
    #print(json.dumps(PrintTable))                      #DELETE
    ExportNiceTable(PrintTable) #empy method
    return PrintTable

#EMPTY METHOD, FOR OVERRIDING 
# you can import this file in other .py file and overdrive this method
#for example to export PrintTable from NiceTable() in json or in plain text for printing on paper
def ExportNiceTable(PrintTable):
    return

def Tick():
    #firstly SetBorder() - that returns [obj, obj] of changed Cells{}
    #then FindPath()
    #by the result of FindPath(), it is needed to call obj.SetBorderConfirm() on [obj, obj]
    #if path is found -> obj.SetBorderConfirm(True) -> next tick
    #if path is not found -> obj.SetBorderConfirm(False) -> try again from SetBorder()
    #if SetBorder() cant be done, then return and the maze is done
    objList = []
    pathResult = None

    objList = SetBorder()
    if( not objList): return False #maze is done (no other border can be set)

    pathResult = FindPath()
    if(pathResult and NoIsolated() == 0):     #path exists && there are no isolated cells
        for obj in objList:
            obj.SetBorderConfirm(True)
    else:               #path does not exist || there are some isolated cells
        for obj in objList:
            obj.SetBorderConfirm(False)

    return True

def Initialize(size):
    neighborsMatrix = []
    global StartingCell
    global FinalCell
    Cells.clear() #resets Cells[] for when script runs more than 1 time

    def returnNeighbors(i, j):
        try:
            if(i < 0 or j < 0): raise IndexError("negative indexing in use")
            return neighborsMatrix[i][j]
        except IndexError:
            return False
    def returnBorder(i, j):
        if returnNeighbors(i, j):
            return -1
        else:
            return 1
    
    #CREATE CELLS & SET POSITIONS
    for h in range(size[1]):
        for w in range(size[0]):
            x = Cell([w, h])
            #x.position.initialize([w, h])

    #SET NEIGHBORS and CORESPONDING BORDERS!! - to be implemented
    for x in range(0, len(Cells), size[0]):
        neighborsMatrix.append(Cells[x:x+size[0]])
    
    for i in range(len(neighborsMatrix)):
        for j in range(len(neighborsMatrix[0])):
            neighborsMatrix[i][j].neighbors = [returnNeighbors(i, j+1), returnNeighbors(i-1, j), returnNeighbors(i, j-1), returnNeighbors(i+1, j)]
            neighborsMatrix[i][j].border = [returnBorder(i, j+1), returnBorder(i-1, j), returnBorder(i, j-1), returnBorder(i+1, j)]

    #SET StartingCell & FinalCell
    StartingCell = Cells[0]
    FinalCell = Cells[-1]


    return True    

def Run(size, sleep):
    width = size[0]
    height = size[1]
    iteration = 0

    Initialize([width, height])

    while(True):
        iteration += 1
        if sleep > 0:
            Show(iteration)
            time.sleep(sleep)
        if( not Tick()): break
    Show(iteration)

    print(f"MAZE DONE in {iteration} iterations")


class Cell:
    def __init__(self, coordinates):
        Cells.append(self)
        
        self.position = Position(coordinates) #object Position{}
        self.neighbors = None #list [Object, Object, Object, Object] - right, upper, left, bottom
        self.border = None #list [-1, -1, 0, 1] - right, upper, left, bottom; -1 unset (not border), 0 not border, 1 border

        self.lastCheckedNeighbor = -1 #int (index of neighbors[]), get resets every FindPath()
        self.lastChangedBorder = -1 #set by self.SetBorder() and reset by self.SetBorderConfirm()
    def __str__(self):
        return f"cell object on position: {str(self.position.get())}"

    def Path(self, previousCell): #previousCell also cannot be on the path
        #print(f"self.Path() : {self.position.get(), self.lastCheckedNeighbor, self.border}") #DEBUGGING
        if(self.lastCheckedNeighbor == 3):
            return False
        else:
            self.lastCheckedNeighbor += 1
            #if(self.border[self.lastCheckedNeighbor] < 1):
            #    return self.neighbors[self.lastCheckedNeighbor]
            #else:
            #    return self.Path()

            if(self.border[self.lastCheckedNeighbor] == 1 or self.neighbors[self.lastCheckedNeighbor] == previousCell):
                return self.Path(previousCell)
            else:
                return self.neighbors[self.lastCheckedNeighbor]

    def Border(self): #if border cannot be set, return False, if border was set, return self and neighbor (so that obj,SetBorderConfirm() can be called on both)
        def inner():
            index = random.randint(0, 3)
            if(self.border[index] == 1): #if self.border[index] is already set, try other one
                return inner()
            elif(self.border.count(1) > 2 or self.neighbors[index].border.count(1) > 2): #if no other border can be set, return False
                self.CloseBorder()
                self.neighbors[index].CloseBorder()
                return False
            else:
                direction = Direction(index)

                previousBorder = self.border.copy()
                self.SetBorder(direction.get())                 #set border for self
                self.neighbors[index].SetBorder(direction.op()) #set border for neighbor
                #return self and neighbor
                return [self, self.neighbors[index]]
        return inner()

    #METHOD FOR SETTING BORDER - self.border set True & self.neighbors set False
    def SetBorder(self, i): #i (0,3) - right, upper, left, bottom
        self.border[i] = 1
        #self.neighbors[i] = False
        self.lastChangedBorder = i
        
        #print(f"SetBorder: {str(self.position.get()), i, self.border}") #DEBUGGING
    def SetBorderConfirm(self, input): #input True - path was found, False - path was not found
        if(input):
            self.lastChangedBorder = -1 #reset value
        else:
            self.border[self.lastChangedBorder] = 0
            self.lastChangedBorder = -1

        #print(f"SetBorderConfirm: {str(self.position.get()), input, self.border}") #DEBUGGING
    def CloseBorder(self): #if self.border is [-1, 1, 1, 1], this method -> [0, 1, 1, 1]
        for i in range(len(self.border)):
            if self.border[i] == -1:
                self.border[i] = 0



class Position:
    def __init__(self, coordinates = False):
        self.x = None #int
        self.y = None#int
        if(coordinates): self.initialize(coordinates)
    def initialize(self, coordinates):
        self.x = coordinates[0]
        self.y = coordinates[1]
    def get(self):
        return [self.x, self.y]
    def compare(self, coordinates):
        if(self.x == coordinates[0] and self.y == coordinates[1]): 
            return True
        else:
            return False
    def neighbor(self, direction): #int (0,3) - right, upper, left, bottom
        if(direction == 0):
            return [self.x + 1, self.y]
        elif(direction == 1):
            return [self.x, self.y + 1]
        elif(direction == 2):
            return [self.x - 1, self.y]
        elif(direction == 3):
            return [self.x, self.y - 1]
        else:
            return False

class Direction:
    def __init__(self, value):
        self.value = value #int (0,3) - right, upper, left, bottom
    def get(self):
        return self.value
    def rot(self): #rotate direction by +90°
        if(self.value == 3):
            self.value = 0
        else:
            self.value += 1
        return self.get()
    def op(self): #oposite = rotate direction by +180°
        self.rot()
        self.rot()
        return self.get()


class Tests:
    def __init__(self, test, size):
        size = [3, 3]
        
        Initialize([size[0], size[1]])
        Cells[0].border = [1, 1, 1, 0]
        Cells[1].border = [0, 1, 1, 1]
        Cells[2].border = [1, 1, 0, 0]
        Cells[3].border = [1, 0, 1, 0]
        Cells[4].border = [1, 1, 1, 1]
        Cells[5].border = [1, 0, 1, 1]
        Cells[6].border = [0, 0, 1, 1]
        Cells[7].border = [1, 1, 0, 1]
        Cells[8].border = [1, 1, 1, 1]
        Show(0)
        
        #self.path()
        self.isolated()
    def path(self):
        print(FindPath())
    def isolated(self):
        print(NoIsolated())





if __name__ == "__main__":
  #Run([35, 10], 0.05)
  Run([10, 10], 0.05)
  #t = Tests(1, [3, 3])