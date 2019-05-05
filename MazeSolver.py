from PIL import Image
from Point import Point
from collections import deque
import time

imagePath = "./Mazes/4999x4999.bmp"
imageName = imagePath[8:-4]

createdPoints = []
loopOperations = 0

lastLeft = (-1, -1) # (col, index in created points)
lastSeenVertical = [] # [(row, index in created points)]

imageWidth = 0
imageHeight = 0

def startSolver():
    # First, we need to import an image
    # TODO add asking what size to pick when starting the program

    global lastSeenVertical, imageHeight, imageWidth

    print(imageName)

    image = Image.open(imagePath)
    imageWidth, imageHeight = image.size

    pixels = image.load()
    mazeArray = []
    
    timeStart = time.time()

    for i in range(imageHeight):
        rowArray = []
        for k in range(imageWidth):
            rowArray.append(pixels[k, i])
        mazeArray.append(rowArray)

    print("--- Maze array creation = %s seconds ---" % (time.time() - timeStart))

    timeStart = time.time()
    newArr = findImportantPointsInMaze(mazeArray)
    print("--- Find important points = %s seconds ---" % (time.time() - timeStart))
    
    # Fill last seen array
    lastSeenVertical = [(-1, -1)] * len(newArr)

    timeStart = time.time()

    connectPoints(newArr)

    print("--- Connect Points = %s seconds ---" % (time.time() - timeStart))

    print("Number of loop Operations = " + str(loopOperations))

    timeStart = time.time()
    path = breadthFirstSearch()
    print("--- Breadth First Search = %s seconds ---" % (time.time() - timeStart))


    # for point in path:
    #     print(point)

    # Save path to bitmap
    newImage = image.convert('RGB')
    newPixels = newImage.load()
    pathToBitmap(newImage, newPixels, path)


def breadthFirstSearch():
    global imageWidth, imageHeight
    startPoint, endPoint = createdPoints[0], createdPoints[len(createdPoints) -1]
    queue = deque([startPoint])

    prev = [None] * (imageHeight * imageWidth)
    visited = [False] * (imageHeight * imageWidth)

    visited[startPoint.getRow() * imageWidth + startPoint.getCol()] = True

    completed = False

    while len(queue) > 0:
        cur = queue.pop()
        if(cur.getIsFinish()):
            completed = True
            break
        
        for n in cur.neighbors:
            if n != None:
                npos = n.getRow() * imageWidth + n.getCol()
                if visited[npos] == False:
                    queue.appendleft(n)
                    visited[npos] = True
                    prev[npos] = cur


    print('as')
    path = deque()
    cur = endPoint
    while (cur != None):
        path.appendleft(cur)
        cur = prev[cur.getRow() * imageWidth + cur.getCol()]
        

    return path


def connectPoints(arr):
    # TODO maybe make a better algorithm
    global lastLeft
    global loopOperations

    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if(arr[row][col] == 2):
                # First make a new point
                newPoint = Point(row, col)
                if(row == 0):
                    newPoint.setIsStart(True)
                elif(row == len(arr) - 1):
                    newPoint.setIsFinish(True)
                createdPoints.append(newPoint)

                # If last left is -1, this is the first point in the row
                if(lastLeft[0] != -1):
                    # loop backwards to make sure the points can connect
                    # tempCol = col -1
                    # doesConnect = True
                    # while tempCol != lastLeft[0]:
                    #     loopOperations += 1
                    #     if(arr[row][tempCol] == 1):
                    #         doesConnect = False
                    #     tempCol -= 1

                    # if(doesConnect):
                        # Set links between the two points
                    createdPoints[len(createdPoints) - 1].setLeft(createdPoints[lastLeft[1]])
                    createdPoints[lastLeft[1]].setRight(createdPoints[len(createdPoints) - 1])

                lastLeft = (col, len(createdPoints) - 1)
                
                # If last seen vertical is -1, this is the first point in the col
                if(lastSeenVertical[col][0] != -1):
                    # loop upward to make sure the points can connect
                    tempRow = row - 1
                    doesConnect = True
                    while tempRow != lastSeenVertical[col][0]:
                        loopOperations += 1
                        if(arr[tempRow][col] == 1):
                            doesConnect = False
                        tempRow -= 1

                    if(doesConnect):
                        createdPoints[len(createdPoints) - 1].setUp(createdPoints[lastSeenVertical[col][1]])
                        createdPoints[lastSeenVertical[col][1]].setDown(createdPoints[len(createdPoints) - 1])

                lastSeenVertical[col] = (row, len(createdPoints) - 1)
            elif(arr[row][col] == 1):
                lastLeft = (-1, -1)
        lastLeft = (-1, -1)


def findImportantPointsInMaze(arr):
    global loopOperations
    # Go through each point and check if it's an important point. If it is, make it a 2 in a new maze
    newMaze = []
    for row in range(len(arr)):
        newRow = []
        for col in range(len(arr[row])):
            if(arr[row][col] != 1 and isImportantPoint(arr, row, col)):
                newRow.append(2)
            else:
                newRow.append(arr[row][col])

        newMaze.append(newRow)

    return newMaze


def isImportantPoint(arr, row, col):
    # Algorithm: If a point in the maze only has 1 horizontal or vertical passage, then it's an important point
    #            Also if a point has a passage on all 4 sides, it's important point

    # Keep track of passages on the horizontal and vertical planes
    hPassages = 0
    vPassages = 0
    # printArray(arr)

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

    # print(row, col, hPassages, vPassages)

    # Do final check on number of passages
    if(hPassages == 1 or vPassages == 1 or (hPassages + vPassages) == 4):
        return True

    return False


def printArray(arr):
    for i in range(len(arr)):
        for k in range(len(arr[i])):
            print(arr[i][k], end=" ")
        print()


def pathToBitmap(image, arr, path):
    global imagePath
    imageWidth, imageHeight = image.size

    # Draw in between points
    for i in range(len(path) - 1):
        hDif = path[i+1].getCol() - path[i].getCol()
        vDif = path[i+1].getRow() - path[i].getRow()
        # print(hDif, vDif)

        if(hDif != 0): # the two points connect horizontally
            if(hDif < 0):
                while hDif != 0:
                    arr[path[i].getCol() + hDif +1, path[i].getRow()] = (255, 0, 0)
                    hDif += 1
            if(hDif > 0):
                while hDif != 0:
                    arr[path[i].getCol() + hDif-1, path[i].getRow()] = (255, 0, 0)
                    hDif -= 1
        elif(vDif != 0):
            if(vDif < 0):
                while vDif != 0:
                    arr[path[i].getCol(), path[i].getRow() + vDif+1] = (255, 0, 0)
                    vDif += 1
            if(vDif > 0):
                while vDif != 0:
                    arr[path[i].getCol(), path[i].getRow() + vDif-1] = (255, 0, 0)
                    vDif -= 1

    arr[path[len(path)-1].getCol(), path[len(path)-1].getRow()] = (255, 0, 0)

    image.save("./Results/" + imageName + "_path.png")


if __name__ == '__main__':
    startSolver()
