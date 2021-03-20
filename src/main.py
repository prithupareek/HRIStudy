# import the pygame module, so you can use it
import pygame as pg
from pygame import mouse

# some constants
EMPTY = 0
SELCTED = 1
CROSSED = 2

class Nonogram(object):
    def __init__(self, screen, puzzleName) -> None:
        self.rows = 10
        self.cols = 10

        self._screen = screen
        self._width, self._height = self._screen.get_size()

        self._cellDims = 50
        self._gridColor = (0, 0, 0)

        self._crossImg = pg.image.load('assets/cross.png')
        self._crossImg = pg.transform.scale(self._crossImg, (self._cellDims - 10, self._cellDims - 10))

        self.gameState = [[0 for col in range(self.cols)] for row in range(self.rows)]
        # self.prettyPrintGameState()

        self.puzzle = self.loadPuzzle(puzzleName)

    def loadPuzzle(self, puzzleName):
        puzzleFilePath = "puzzles/" + puzzleName + ".txt"
        puzzleFile = open(puzzleFilePath, "r")
        
        puzzleData = []

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

        return puzzleData

                    


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
        if (row, col) != (-1, -1):
            # modify the game state appropriately
            self.gameState[row][col] = (self.gameState[row][col] + 1) % 3

            # self.prettyPrintGameState()



    def draw(self):
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

                if self.gameState[row][col] == SELCTED:
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
                    


    def update(self, keys):
        pass

class Game(object):
    def __init__(self) -> None:
        # initialize the pygame module
        pg.init()
        pg.display.set_caption("HRI Study")
        pg.font.init()

        # create a fullscreen window for pygame to run
        self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # define a variable to control the main loop
        self._running = True

        self._keys = pg.key.get_pressed()

        self._nonogram = Nonogram(self._screen, "testPuzzle")

    def eventLoop(self):
        for event in pg.event.get():
            self._keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self._keys[pg.K_ESCAPE]:
                self._running = False
            if event.type == pg.MOUSEBUTTONUP:
                self._nonogram.mousePressed()

    def draw(self):
        self._screen.fill(pg.Color("white"))
        self._nonogram.draw()

    def update(self):
        self._nonogram.update(keys=self._keys)

    def mainLoop(self) -> None:
        # main loop
        while self._running:
            self.eventLoop()
            self.update()
            self.draw()
            pg.display.update()
 
# define a main function
def main():
     game = Game()
     game.mainLoop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()