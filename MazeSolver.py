from PIL import Image
from Point import Point
from collections import deque
import time

imagePath = "./Mazes/4999x4999.png"
imageName = imagePath[8:-4]

createdPoints = []
loopOperations = 0

lastLeft = (-1, -1) # (col, index in created points)
lastSeenVertical = [] # [(row, index in created points)]

imageWidth = 0
imageHeight = 0

mazeStart = None
mazeEnd = None

def startSolver():
    # First, we need to import an image
    # TODO add asking what size to pick when starting the program

    global lastSeenVertical, imageHeight, imageWidth

    print(imageName)

    image = Image.open(imagePath)
    imageWidth, imageHeight = image.size

    timeStart = time.time()

    # OLD STUFF
    # pixels = image.load()
    # mazeArray = []
    # for i in range(imageHeight):
    #     rowArray = []
    #     for k in range(imageWidth):
    #         rowArray.append(pixels[k, i])
    #     mazeArray.append(rowArray)

    pixels = list(image.getdata(0))
    maze = newMazeCreation(pixels)

    # for i in createdPoints:
    #     print(i)


    print("--- Maze array creation = %s seconds ---" % (time.time() - timeStart))

    print("Node Count: " + str(len(createdPoints)))
    
    # print("Number of loop Operations = " + str(loopOperations))

    timeStart = time.time()
    path = breadthFirstSearch()
    print("--- Breadth First Search = %s seconds ---" % (time.time() - timeStart))

    # Save path to bitmap
    newImage = image.convert('RGB')
    newPixels = newImage.load()
    pathToBitmap(newImage, newPixels, path)


def newMazeCreation(pixels):
    global imageWidth, imageHeight
    lLeft = None
    aboveList = [None] * imageWidth
    

    for topRowIndex in range(imageWidth):
        if(pixels[topRowIndex] == 255): # Start of the maze
            newPoint = Point(0, topRowIndex)
            newPoint.isStart = True
            mazeStart = newPoint
            aboveList[topRowIndex] = newPoint
            createdPoints.append(newPoint)

        # if(pixels[imageWidth * (imageHeight - 1) + topRowIndex] == 255): # End of the Maze
        #     newPoint = Point(imageHeight - 1, topRowIndex)
        #     newPoint.isFinish = True
        #     mazeEnd = newPoint
        #     createdPoints.append(newPoint)

    for i in range(imageWidth, len(pixels)):
        row = int(i / imageHeight)
        col = i % imageWidth

        if(pixels[i] == 0):
            lLeft = None
            aboveList[col] = None

        elif(pixels[i] != 0): # Only do something if a passage is found
            
            left = pixels[i-1]
            right = pixels[i+1]

            up = 0
            down = 0
            if(i > imageWidth):
                up = pixels[i-imageWidth]
            if(i < (imageWidth * imageHeight) - imageWidth):
                down = pixels[i+imageWidth]

            # determine if important
            hPassage = int((left + right) / 255)
            vPassage = int((up + down) / 255)
            # print("Pos: ", row, col)
            # print("pCount: ", hPassage, vPassage)
            
            if(hPassage == 1 or vPassage == 1 or (hPassage + vPassage == 4)):
                newPoint = Point(row, col)

                if(lLeft != None):
                    lLeft.neighbors[1] = newPoint
                    newPoint.neighbors[0] = lLeft
                    

                if(aboveList[col] != None):
                    newPoint.neighbors[2] = aboveList[col]
                    aboveList[col].neighbors[3] = newPoint
                
                if(row == imageHeight-1):
                    newPoint.isFinish = True
                    mazeEnd = newPoint
                
                
                lLeft = newPoint
                aboveList[col] = newPoint
                createdPoints.append(newPoint)


def breadthFirstSearch():
    global imageWidth, imageHeight
    startPoint, endPoint = createdPoints[0], createdPoints[len(createdPoints) -1]
    queue = deque([startPoint])

    prev = [None] * (imageHeight * imageWidth)
    visited = [False] * (imageHeight * imageWidth)

    visited[startPoint.row * imageWidth + startPoint.col] = True

    completed = False

    while len(queue) > 0:
        cur = queue.pop()
        if(cur.isFinish):
            completed = True
            break
        
        for n in cur.neighbors:
            if n != None:
                npos = n.row * imageWidth + n.col
                if visited[npos] == False:
                    queue.appendleft(n)
                    visited[npos] = True
                    prev[npos] = cur


    path = deque()
    cur = endPoint
    while (cur != None):
        path.appendleft(cur)
        cur = prev[cur.row * imageWidth + cur.col]
        

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
        hDif = path[i+1].col - path[i].col
        vDif = path[i+1].row - path[i].row
        # print(hDif, vDif)

        if(hDif != 0): # the two points connect horizontally
            if(hDif < 0):
                while hDif != 0:
                    arr[path[i].col + hDif +1, path[i].row] = (255, 0, 0)
                    hDif += 1
            if(hDif > 0):
                while hDif != 0:
                    arr[path[i].col + hDif-1, path[i].row] = (255, 0, 0)
                    hDif -= 1
        elif(vDif != 0):
            if(vDif < 0):
                while vDif != 0:
                    arr[path[i].col, path[i].row + vDif+1] = (255, 0, 0)
                    vDif += 1
            if(vDif > 0):
                while vDif != 0:
                    arr[path[i].col, path[i].row + vDif-1] = (255, 0, 0)
                    vDif -= 1

    arr[path[len(path)-1].col, path[len(path)-1].row] = (255, 0, 0)

    image.save("./Results/" + imageName + "_path.png")


if __name__ == '__main__':
    startSolver()
