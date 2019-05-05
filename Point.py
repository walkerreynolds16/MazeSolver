
class Point:

    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.left = None
        self.right = None
        self.up = None
        self.down = None

    def __str__(self):
        resStr = "[" + str(self.row) + ", " + str(self.col) + "] ->"
        if(self.left is not None):
            resStr += " Left: " + self.left.getPointString() + ","
        else:
            resStr += " Left: None, "

        if(self.right is not None):
            resStr += " Right: " + self.right.getPointString() + ","
        else:
            resStr += " Right: None, "

        if(self.up is not None):
            resStr += " Up: " + self.up.getPointString() + ","
        else:
            resStr += " Up: None, "

        if(self.down is not None):
            resStr += " Down: " + self.down.getPointString()
        else:
            resStr += " Down: None"

        return resStr


    def getPointString(self):
        return "[" + str(self.row) + ", " + str(self.col) + "]"

    def getRow(self):
        return self.row

    def getCol(self):
        return self.col

    def getLeft(self):
        return self.left

    def setLeft(self, left):
        self.left = left

    def getRight(self):
        return self.right

    def setRight(self, right):
        self.right = right

    def getUp(self):
        return self.up

    def setUp(self, up):
        self.up = up

    def getdown(self):
        return self.down

    def setDown(self, down):
        self.down = down


    
    