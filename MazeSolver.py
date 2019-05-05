from PIL import Image
from Point import Point
import time
import copy

imagePath = "./Mazes/4999x4999.bmp"

createdPoints = []
loopOperations = 0

lastLeft = (-1, -1) # (col, index in created points)
lastSeenVertical = [] # [(row, index in created points)]

def startSolver():
    # First, we need to import an image
    # TODO add asking what size to pick when starting the program

    global lastSeenVertical

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
    

    timeStart = time.time()

    lastSeenVertical = [(-1, -1)] * len(newArr)

    # printArray(newArr)

    connectPoints(newArr)

    print("--- Connect Points = %s seconds ---" % (time.time() - timeStart))

    print("Number of loop Operations = " + str(loopOperations))

    # for point in createdPoints:
    #     print(point)


def connectPointsSingle(arr, row, col):
    # printArray(arr)
    # if(arr[row][col] == 2):
    #     # First make a new point
    #     newPoint = Point(row, col)
    #     createdPoints.append(newPoint)

        

    #     # If last left is -1, this is the first point in the row
    #     if(lastLeft[0] != -1):
    #         # loop backwards to make sure the points can connect
    #         tempCol = col -1
    #         doesConnect = True
    #         while tempCol != lastLeft[0]:
    #             loopOperations += 1
    #             if(arr[row][tempCol] == 1):
    #                 doesConnect = False
    #             tempCol -= 1

    #         if(doesConnect):
    #             # Set links between the two points
    #             createdPoints[len(createdPoints) - 1].setLeft(createdPoints[lastLeft[1]])
    #             createdPoints[lastLeft[1]].setRight(createdPoints[len(createdPoints) - 1])

    #     lastLeft = (col, len(createdPoints) - 1)
        
    #     # If last seen vertical is -1, this is the first point in the col
    #     if(lastSeenVertical[col][0] != -1):
    #         # loop upward to make sure the points can connect
    #         tempRow = row - 1
    #         doesConnect = True
    #         while tempRow != lastSeenVertical[col][0]:
    #             loopOperations += 1
    #             if(arr[tempRow][col] == 1):
    #                 doesConnect = False
    #             tempRow -= 1

    #         if(doesConnect):
    #             createdPoints[len(createdPoints) - 1].setUp(createdPoints[lastSeenVertical[col][1]])
    #             createdPoints[lastSeenVertical[col][1]].setDown(createdPoints[len(createdPoints) - 1])

    #     lastSeenVertical[col] = (row, len(createdPoints) - 1)
    print()

def connectPoints(arr):
    # TODO maybe make a better algorithm
    global lastLeft
    global loopOperations

    for row in range(len(arr)):
        for col in range(len(arr[row])):
            if(arr[row][col] == 2):
                # First make a new point
                newPoint = Point(row, col)
                createdPoints.append(newPoint)

                # If last left is -1, this is the first point in the row
                if(lastLeft[0] != -1):
                    # loop backwards to make sure the points can connect
                    tempCol = col -1
                    doesConnect = True
                    while tempCol != lastLeft[0]:
                        loopOperations += 1
                        if(arr[row][tempCol] == 1):
                            doesConnect = False
                        tempCol -= 1

                    if(doesConnect):
                        # Set links between the two points
                        createdPoints[len(createdPoints) - 1].setLeft(createdPoints[lastLeft[1]])
                        createdPoints[lastLeft[1]].setRight(createdPoints[len(createdPoints) - 1])

                lastLeft = (col, len(createdPoints) - 1)
                # print(col)
                # print(lastSeenVertical)
                
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


if __name__ == '__main__':
    startSolver()
