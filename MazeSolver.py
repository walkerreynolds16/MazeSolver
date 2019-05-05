from PIL import Image
from Point import Point

imagePath = "./Mazes/999x999.bmp"

createdPoints = []


def startSolver():
    # First, we need to import an image
    # TODO add asking what size to pick when starting the program

    image = Image.open(imagePath)
    imageWidth, imageHeight = image.size

    # pixels = image.convert('RGB').load()
    pixels = image.load()
    # image.show()

    mazeArray = []

    for i in range(imageHeight):
        rowArray = []
        for k in range(imageWidth):
            rowArray.append(pixels[k, i])
        mazeArray.append(rowArray)

    newArr, importantPoints = findImportantPointsInMaze(mazeArray)
    # printArray(newArr)
    print(len(importantPoints))
    # createGraph(newArr, importantPoints)
    print(len(createdPoints))


def createGraph(arr, importantPoints):
    # TODO maybe make a better algorithm

    # Go to each point and find if it's connect in each direction
    # Return a graph object representing the important points in the maze
    for iPoint in importantPoints:
        newPointObj = Point(iPoint[0], iPoint[1])
        createdPoints.append(newPointObj)

        newPointObj.setLeft(findClosestLeftPoint(arr, newPointObj))
        newPointObj.setRight(findClosestRightPoint(arr, newPointObj))
        newPointObj.setUp(findClosestUpPoint(arr, newPointObj))
        newPointObj.setDown(findClosestDownPoint(arr, newPointObj))

        print(newPointObj)
        


def findClosestLeftPoint(arr, point):
    # We know that an important point cannot be on 0th col of the maze, so we don't check for it
    col = point.getCol()-1
    row = point.getRow()

    while col > 0:
        if(arr[row][col] == 1):
            return None
        elif(arr[row][col] == 2):
            createdPoint = findPointInCreatedPoints(row, col)

            if(createdPoint is None):
                return Point(row, col)
            else:
                return createdPoint

        col -= 1


def findClosestRightPoint(arr, point):
    # We know that an important point cannot be on the last col of the maze, so we don't check for it
    col = point.getCol() + 1
    row = point.getRow()

    while col < len(arr[row]):
        if(arr[row][col] == 1):
            return None
        elif(arr[row][col] == 2):
            createdPoint = findPointInCreatedPoints(row, col)

            if(createdPoint is None):
                return Point(row, col)
            else:
                return createdPoint

        col += 1


def findClosestUpPoint(arr, point):
    # We know that an important point cannot be on 0th col of the maze, so we don't check for it
    col = point.getCol()
    row = point.getRow()-1

    while row >= 0:
        if(arr[row][col] == 1):
            return None
        elif(arr[row][col] == 2):
            createdPoint = findPointInCreatedPoints(row, col)

            if(createdPoint is None):
                return Point(row, col)
            else:
                return createdPoint
        
        row -= 1

def findClosestDownPoint(arr, point):
    # We know that an important point cannot be on 0th col of the maze, so we don't check for it
    col = point.getCol()
    row = point.getRow()+1

    while row < len(arr):
        if(arr[row][col] == 1):
            return None
        elif(arr[row][col] == 2):
            createdPoint = findPointInCreatedPoints(row, col)

            if(createdPoint is None):
                return Point(row, col)
            else:
                return createdPoint
        
        row += 1

def findPointInCreatedPoints(row, col):
    for point in createdPoints:
        if(point.getRow() == row and point.getCol() == col):
            return point

    return None


def findImportantPointsInMaze(arr):
    # Go through each point and check if it's an important point. If it is, make it a 2 in a new maze
    newMaze = []
    importantPoints = []
    for row in range(len(arr)):
        newRow = []
        for col in range(len(arr[row])):
            if(arr[row][col] != 1 and isImportantPoint(arr, row, col)):
                newRow.append(2)
                importantPoints.append([row, col])
            else:
                newRow.append(arr[row][col])

        newMaze.append(newRow)

    return newMaze, importantPoints


def isImportantPoint(arr, row, col):
    # Algorithm: If a point in the maze only has 1 horizontal or vertical passage, then it's an important point
    #            Also if a point has a passage on all 4 sides, it's important point

    # Keep track of passages on the horizontal and vertical planes
    hPassages = 0
    vPassages = 0

    # Check if point isn't on the edge of the maze, then check for a passage
    # Vertical passages
    if(row != 0 and arr[row-1][col] == 0):
        vPassages += 1
    if(row != len(arr)-1 and arr[row+1][col] == 0):
        vPassages += 1

    # Horizontal passages
    if(col != 0 and arr[row][col-1] == 0):
        hPassages += 1
    if(col != len(arr)-1 and arr[row][col+1] == 0):
        hPassages += 1

    # Do final check on number of passages
    if(hPassages == 1 or vPassages == 1 or (hPassages + vPassages) == 4):
        return True

    return False


def printArray(arr):
    for i in range(len(arr)):
        for k in range(len(arr[i])):
            print(arr[i][k], end=" ")
        print()


if __name__ == '__main__':
    startSolver()
