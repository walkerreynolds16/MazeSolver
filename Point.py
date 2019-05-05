
class Point:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.isStart = False
        self.isFinish = False
        self.neighbors = [None, None, None, None]

    def __str__(self):
        resStr = "[" + str(self.row) + ", " + str(self.col) + "] ->"
        if(self.neighbors[0] is not None):
            resStr += " Left: " + self.neighbors[0].getPointString() + ","
        else:
            resStr += " Left: None, "

        if(self.neighbors[1] is not None):
            resStr += " Right: " + self.neighbors[1].getPointString() + ","
        else:
            resStr += " Right: None, "

        if(self.neighbors[2] is not None):
            resStr += " Up: " + self.neighbors[2].getPointString() + ","
        else:
            resStr += " Up: None, "

        if(self.neighbors[3] is not None):
            resStr += " Down: " + self.neighbors[3].getPointString()
        else:
            resStr += " Down: None"

        return resStr

    # def __eq__(self, other):
    #     if isinstance(other, self.__class__):
    #         return self.col == other.getCol() and self.row == other.getRow()

    def getPointString(self):
        return "[" + str(self.row) + ", " + str(self.col) + "]"

    # def getIsStart(self):
    #     return self.isStart

    # def setIsStart(self, isStart):
    #     self.isStart = isStart

    # def getIsFinish(self):
    #     return self.isFinish

    # def setIsFinish(self, isFinish):
    #     self.isFinish = isFinish

    # def getRow(self):
    #     return self.row

    # def getCol(self):
    #     return self.col

    # def getLeft(self):
    #     return self.left

    # def setLeft(self, left):
    #     self.left = left
    #     self.neighbors[0] = left

    # def getRight(self):
    #     return self.right

    # def setRight(self, right):
    #     self.right = right
    #     self.neighbors[1] = right

    # def getUp(self):
    #     return self.up

    # def setUp(self, up):
    #     self.up = up
    #     self.neighbors[2] = up

    # def getDown(self):
    #     return self.down

    # def setDown(self, down):
    #     self.down = down
    #     self.neighbors[3] = down


    
    
