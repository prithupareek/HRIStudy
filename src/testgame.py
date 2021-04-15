# import the pygame module, so you can use it
import pygame as pg
from pygame import mouse
from nonogram import Nonogram
from nonogram import PLAYING, SOLVED, TIMEOUT
from advice import Advice
import time 

# for the command line args
import sys
import getopt

# for saving participant data
import csv

# Constants for Trial State
INTRO = 0
PLAYING = 1
ENDSCREEN = 2
END = 3
BREAK = 4
MAXTIME = 15    # minutes
BREAKTIME = 3   # minutes

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
        self.puzzles = ["tutorialPuzzle"]
        self.puzzleIndex = 0
        self.advice = None

        self._nonogram = Nonogram(self._screen, self.puzzles[self.puzzleIndex], self.advice)
        self._startTime = time.time()
        self._solvetimes = []

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

    def draw(self, startTime):
            self._screen.fill(pg.Color("white"))
            self._nonogram.draw(startTime)
    
    def update(self):
        finished = False

        # calculate elapsed time
        elapedTotalSeconds = time.time() - self._startTime - self._nonogram.adviceTimes
        elapsedMinutes = elapedTotalSeconds // 60
        elapsedSeconds = elapedTotalSeconds % 60

        if self._running == PLAYING:
            self._nonogram.update(keys=self._keys)

        # check to see if we advance to next puzzle
        if self._nonogram.gameMode == SOLVED:
            finished = True
        elif self._running == PLAYING and elapsedMinutes >= MAXTIME: # puzzle is taking longer than 10 minutes
            finished = True
        elif self._running == BREAK and elapsedMinutes >= BREAKTIME: # break is over
            finished = True

        if finished:
            if self._running == PLAYING:
                # add to solve times
                self._solvetimes.append(elapedTotalSeconds//1)
                # print out completion time to console
                print("Puzzle " + str(self.puzzleIndex) +" Completed Time: {0:02}:{1:02}".format(int(elapsedMinutes), int(elapsedSeconds//1)))
                self.puzzleIndex += 1
                if self.puzzleIndex >= len(self.puzzles):
                    self._running = ENDSCREEN
                else:
                    self._running = BREAK
                    self._nonogram = Nonogram(self._screen, self.puzzles[self.puzzleIndex], self.advice)
                    self._startTime = time.time()
            elif self._running == BREAK:
                self._running = PLAYING
                self._startTime = time.time()

    def mainLoop(self) -> None:
        # main loop
        first = True
        while self._running != END:
            self.eventLoop()
            if self._running == PLAYING:
                # set time to begin at the start of puzzle
                if first:
                    self._startTime = time.time()
                    first = False
                self.update()
            self.draw(self._startTime)
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
