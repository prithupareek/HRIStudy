# import the pygame module, so you can use it
import pygame as pg
from pygame import mouse
from nonogram import Nonogram
from nonogram import PLAYING, SOLVED, TIMEOUT

# Constants for Trial State
INTRO = 0
PLAYING = 1
ENDSCREEN = 2
END = 3

class Game(object):
    def __init__(self) -> None:
        # initialize the pygame module
        pg.init()
        pg.display.set_caption("HRI Study")
        pg.font.init()

        # create a fullscreen window for pygame to run
        self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # define a variable to control the main loop
        self._running = INTRO

        self._keys = pg.key.get_pressed()
    
        # Multiple puzzles
        self.puzzles = ["testPuzzle", "testPuzzle"]
        self.puzzleIndex = 0
        self._nonogram = Nonogram(self._screen, self.puzzles[self.puzzleIndex])

    def eventLoop(self):
        for event in pg.event.get():
            self._keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self._keys[pg.K_ESCAPE]:
                self._running = END
            if event.type == pg.MOUSEBUTTONUP:
                if self._running == PLAYING:
                    self._nonogram.mousePressed()
                elif self._running == INTRO:
                    self._running = PLAYING

    def draw(self):
        self._screen.fill(pg.Color("white"))
        self._nonogram.draw()

    def drawIntro(self):
        self._screen.fill(pg.Color("blue"))
    
    def drawEnd(self):
        self._screen.fill(pg.Color("red"))

    def update(self):
        self._nonogram.update(keys=self._keys)
        if self._nonogram.gameMode == SOLVED:
            self.puzzleIndex += 1
            if self.puzzleIndex >= len(self.puzzles):
                self._running = ENDSCREEN
            else:
                self._nonogram = Nonogram(self._screen, self.puzzles[self.puzzleIndex])

    def mainLoop(self) -> None:
        # main loop
        while self._running == INTRO:
            self.eventLoop()
            self.drawIntro()
            pg.display.update()
        while self._running == PLAYING:
            self.eventLoop()
            self.update()
            self.draw()
            pg.display.update()
        while self._running == ENDSCREEN:
            self.eventLoop()
            self.drawEnd()
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