# import the pygame module, so you can use it
import pygame as pg
import time

# some constants
EMPTY = 0
SELECTED = 1
CROSSED = 2

PLAYING = 0
SOLVED = 1
TIMEOUT = 2

class Nonogram(object):
    def __init__(self, screen, puzzleName, advice) -> None:
        self.rows = 8
        self.cols = 8

        self._screen = screen
        self._width, self._height = self._screen.get_size()

        self._cellDims = 50
        self._gridColor = (0, 0, 0)

        self._crossImg = pg.image.load('assets/cross.png')
        self._crossImg = pg.transform.scale(self._crossImg, (self._cellDims - 10, self._cellDims - 10))

        self.gameState = [[0 for col in range(self.cols)] for row in range(self.rows)]
        # self.prettyPrintGameState()

        self.gameMode = PLAYING
        
        self.advice = advice
        
        self.puzzle, self.solutionState = self.loadPuzzle(puzzleName)

        # Variables for determining advice
        self.adviceCounts = 0
        self.lastClickTime = None
        self.countFourth = False
        self.countHalf = False
        self.countThreeFourth = False

        self.adviceTimes = 0
        self.currentAdviceDiagram = None

        self.counter = None # advice delay

    def loadPuzzle(self, puzzleName):
        puzzleFilePath = "puzzles/" + puzzleName + ".txt"
        puzzleFile = open(puzzleFilePath, "r")
        
        puzzleData = []
        solution = [[0 for col in range(self.cols)] for row in range(self.rows)]

        # keep track of row cols for solution
        row = 0
        col = 0 

        # Loop through the file line by line
        for line in puzzleFile:
            # ignore comments
            if line.startswith('#'):
                continue

            # for puzzle data
            if line.startswith('('):
                # loop through each cell
                for cell in line.split(", "):
                    # remove extra chars around
                    striped = cell.strip()
                    converted = eval(striped)
                    puzzleData += [converted]

            # for solution state
            if line.startswith('|'):
                truncated = line[2:].strip()
                
                for num in truncated.split(" "):
                    num = num.strip()
                    # print(num)
                    solution[row][col] = int(num)
                    col += 1
                
                col = 0
                row += 1

        return puzzleData, solution


    def prettyPrintGameState(self):
        for row in range(self.rows):
            for col in range(self.cols):
                print(self.gameState[row][col], end=" ")
            print('')
        print('')

    def getCellFromPos(self, pos):
        mouseX, mouseY = pos

        # calculate the starting location for the grid
        outerW = self.cols * self._cellDims
        outerH = self.rows * self._cellDims
        outerX = self._width/2 - outerW/2 + (3/2) * self._cellDims
        outerY = self._height/2 - outerH/2 + (3/2) * self._cellDims

        # very ineffeficient, but should get the job done
        # loop through all cells and see if mouse pos is in bounds
        for row in range(self.rows):
            for col in range(self.cols):
                xMin = outerX + col * self._cellDims
                xMax = xMin + self._cellDims
                yMin = outerY + row * self._cellDims
                yMax = yMin + self._cellDims

                if xMin < mouseX < xMax and yMin < mouseY < yMax:
                    return (row, col)
        
        # No cell found
        return (-1, -1)

    def mousePressed(self):
        # get the position of the mouse click
        pos = pg.mouse.get_pos()

        # get the cell clicked
        row, col = self.getCellFromPos(pos)

        # if clicked in grid
        if (row, col) != (-1, -1) and (self.advice == None or (self.advice.p == None or not self.advice.p.is_alive())):
            # modify the game state appropriately
            self.gameState[row][col] = (self.gameState[row][col] + 1) % 3
            self.lastClickTime = time.time()
            # self.prettyPrintGameState()


    def draw(self, startTime):

        # show the diagram while advice is being given
        if self.advice != None and self.advice.p != None and self.advice.p.is_alive():
            self._screen.fill(pg.Color("white"))
            diagram = pg.image.load(self.currentAdviceDiagram)
            diagram = pg.transform.scale(diagram, (int(2*self._width/3), int(2*self._height/3)))
            self._screen.blit(diagram, 
                              (int(self._width/2 - diagram.get_rect().width/2), 
                               int(self._height/2 - diagram.get_rect().height/2)))
            self.lastClickTime = time.time()
        # show the game
        else:
            # Draw the outer rectangle 
            outerW = self.cols * self._cellDims
            outerH = self.rows * self._cellDims
            outerX = self._width/2 - outerW/2 + (3/2) * self._cellDims
            outerY = self._height/2 - outerH/2 + (3/2) * self._cellDims
            pg.draw.rect(self._screen, self._gridColor, pg.Rect(outerX, outerY, outerW, outerH),  2) 

            # Draw the grid
            for row in range(self.rows):
                for col in range(self.cols):
                    x = outerX + col * self._cellDims
                    y = outerY + row * self._cellDims
                    pg.draw.rect(self._screen, self._gridColor, pg.Rect(x, y, self._cellDims, self._cellDims),  2) 

            # draw the side wings of the board
            for row in range(self.rows):
                x = outerX - 3 * self._cellDims
                y = outerY + row * self._cellDims
                w = self._cellDims * 3
                h = self._cellDims
                pg.draw.rect(self._screen, self._gridColor, pg.Rect(x, y, w, h),  2) 

            # draw the top wings of the board
            for col in range(self.cols):
                y = outerY - 3 * self._cellDims
                x = outerX + col * self._cellDims
                h = self._cellDims * 3
                w = self._cellDims
                pg.draw.rect(self._screen, self._gridColor, pg.Rect(x, y, w, h),  2) 

            # draw the state of each cell
            for row in range(self.rows):
                for col in range(self.cols):
                    x = outerX + col * self._cellDims
                    y = outerY + row * self._cellDims

                    if self.gameState[row][col] == SELECTED:
                        pg.draw.rect(self._screen, self._gridColor, pg.Rect(x + 5, y + 5, self._cellDims - 10, self._cellDims - 10)) 
                    elif self.gameState[row][col] == CROSSED:                    
                        self._screen.blit(self._crossImg, (x + 5,y + 5))

            font = pg.font.SysFont('Helvetica', 30)

            # draw the numbers
            for i in range(len(self.puzzle)):
                for j in range(len(self.puzzle[0])):
                    # if not zero
                    if self.puzzle[i][j] != 0:
                        textSurf = font.render(str(self.puzzle[i][j]), False, (0, 0, 0))
                        textRect = textSurf.get_rect()
                        # if on top row
                        if i < len(self.puzzle)/2:
                            # text surface object
                            x = outerX + i * self._cellDims + textRect.height/2
                            y = outerY + j * self._cellDims - self._cellDims*(3) + textRect.width/2

                        # if on side
                        else:
                            y = outerY + (i % self.rows) * self._cellDims + textRect.height/2
                            x = outerX + j * self._cellDims - self._cellDims*(3) + textRect.width/2
                        
                        # draw on the screen
                        self._screen.blit(textSurf, (x, y))
            if self.advice != None:
                ## draw the timer
                #  drawing box for timer
                # pg.draw.rect(self._screen, self._gridColor, pg.Rect(outerX + outerW, outerY + outerH, self._cellDims * 3, self._cellDims * 2),  2) 
                elapedTotalSeconds = time.time() - startTime - self.adviceTimes
                elapsedMinutes = elapedTotalSeconds // 60
                elapsedSeconds = elapedTotalSeconds % 60
                elapsedTime_string = "Time: {0:02}:{1:02}".format(int(elapsedMinutes), int(elapsedSeconds//1))
                timeSurf = font.render(elapsedTime_string, False, (0, 0, 0))
                # timeRect = timeSurf.get_rect()
                self._screen.blit(timeSurf, (outerX + outerW + self._cellDims * 2, outerY))

    def checkWin(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if self.solutionState[row][col] == SELECTED and self.gameState[row][col] != SELECTED:
                    return False
                elif self.solutionState[row][col] == CROSSED and self.gameState[row][col] == SELECTED:
                    return False
        return True

    # Gets a count of the number of placed cells
    def getPlacedCount(self):
        count = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if self.gameState[row][col] != EMPTY:
                    count += 1
        return count

    # Decide when to give advice
    def adviceNeeded(self):
        if self.adviceCounts >= 3:
            return False
        count = self.getPlacedCount()
        # If participant is 1/4 done
        if count == int(self.rows*self.cols/4) and not self.countFourth:
            self.countFourth = True
            self.adviceCounts += 1
            return True
        # If participant place 1/2 of blocks
        if count == int(self.rows*self.cols/2) and not self.countHalf:
            self.countHalf = True
            self.adviceCounts += 1
            return True
        # If participant place 3/4 of blocks
        if count == int(3/4*self.rows*self.cols) and not self.countThreeFourth:
            self.countThreeFourth = True
            self.adviceCounts += 1
            return True
        # Otherwise, if has been 45 sec since last click
        if self.lastClickTime is not None and time.time() - self.lastClickTime > 45: 
            self.lastClickTime = None
            self.adviceCounts += 1
            return True
        return False

    def update(self, keys):
        if self.counter is not None:
            self.counter += 1
            if self.counter > 50:
                advice, self.currentAdviceDiagram = self.advice.giveAdvice(self)
                # used to remove time taken by advice
                self.adviceTimes += advice
                print(self.adviceTimes)
                self.counter = None
        elif self.advice != None and self.adviceNeeded():
            self.counter = 0
        if self.checkWin():
            self.gameMode = SOLVED
