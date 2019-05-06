from PIL import Image
from Point import Point
from collections import deque
import time
import sys

imagePath = "./Mazes/15k.png"
imageName = imagePath[8:-4]

createdPoints = []

imageWidth = 0
imageHeight = 0

mazeStart = None
mazeEnd = None

def startSolver():
    # First, we need to import an image
    # TODO add asking what size to pick when starting the program

    global lastSeenVertical, imageHeight, imageWidth

    print("Image Chosen: " imageName)

    Image.MAX_IMAGE_PIXELS = sys.maxsize
    image = Image.open(imagePath)
    imageWidth, imageHeight = image.size

    timeStart = time.time()

    pixels = list(image.getdata(0))
    maze = newMazeCreation(pixels)
    print("--- Maze array creation = %s seconds ---" % (time.time() - timeStart))

    print("Node Count: " + str(len(createdPoints)))

    timeStart = time.time()
    path = breadthFirstSearch()
    print("--- Breadth First Search = %s seconds ---" % (time.time() - timeStart))

    # Save path to bitmap
    timeStart = time.time()
    newImage = image.convert('RGB')
    newPixels = newImage.load()
    pathToBitmap(newImage, newPixels, path)
    print("--- Saving Image = %s seconds ---" % (time.time() - timeStart))

def newMazeCreation(pixels):
    global imageWidth, imageHeight
    # Last left variable. Keeps track of the last left node found so it can be connected to a new node
    # Used to connect nodes from left and right
    lLeft = None
    # Above list keeps track of the last node created in each col. Used to connect nodes from above and below
    aboveList = [None] * imageWidth
    
    # Go through the top of the maze and find the beginning of the maze and set all the variables
    for topRowIndex in range(imageWidth):
        if(pixels[topRowIndex] == 255): # Start of the maze
            newPoint = Point(0, topRowIndex)
            newPoint.isStart = True
            mazeStart = newPoint
            aboveList[topRowIndex] = newPoint
            createdPoints.append(newPoint)
            break

    # Go through each point in the maze other than the top row and find important parts of the maze
    for i in range(imageWidth, len(pixels)):
        # Since the pixel array is a 1 dimension representation of the image, we can calculated the row and col by doing a little math
        row = int(i / imageHeight)
        col = i % imageWidth

        # if a pixel has a value of 0, its a wall and the last left and last above nodes can be reset
        if(pixels[i] == 0):
            lLeft = None
            aboveList[col] = None

        # If the pixel value is not 0, then a passage has been found, but not all passages are important
        elif(pixels[i] != 0): 
            # get the pixels values around the current pixel
            left = pixels[i-1]
            right = pixels[i+1]

            up = 0
            down = 0
            if(i > imageWidth):
                up = pixels[i-imageWidth]
            if(i < (imageWidth * imageHeight) - imageWidth):
                down = pixels[i+imageWidth]

            # Determine if current pixel is important
            # If a point in the maze only has 1 horizontal or vertical passage, then it's an important point
            # Also if a point has a passage on all 4 sides, it's important point
            hPassage = int((left + right) / 255)
            vPassage = int((up + down) / 255)            
            if(hPassage == 1 or vPassage == 1 or (hPassage + vPassage == 4)):
                # Current pixel is important, make a new node and connect it to other nodes
                newPoint = Point(row, col)

                # If last left is None, then the current node can't be connect to the left
                if(lLeft != None):
                    # If there is a last left, connect the current node's left to last left and connect last left's right node to current
                    lLeft.neighbors[1] = newPoint
                    newPoint.neighbors[0] = lLeft
                    
                # Same thing as connecting left node, do for the above node
                if(aboveList[col] != None):
                    newPoint.neighbors[2] = aboveList[col]
                    aboveList[col].neighbors[3] = newPoint
                
                # Check if the current node is the end of the maze
                if(row == imageHeight-1):
                    newPoint.isFinish = True
                    mazeEnd = newPoint
                
                # Set all variables for the next possible node
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
