# import the pygame module, so you can use it
import pygame as pg
from pygame import mouse
from nonogram import Nonogram

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