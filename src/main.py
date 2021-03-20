# import the pygame module, so you can use it
import pygame as pg

class Nonogram(object):
    def __init__(self) -> None:
        self.rows = 10
        self.cols = 10

        self._cellDims = 50
        self._gridColor = (0, 0, 0)

    def draw(self, screen):
        # get the dimentions of the screen
        screenW, screenH = screen.get_size()

        # Draw the outer rectangle 
        outerW = self.cols * self._cellDims
        outerH = self.rows * self._cellDims
        outerX = screenW/2 - outerW/2 + (3/2) * self._cellDims
        outerY = screenH/2 - outerH/2 + (3/2) * self._cellDims
        pg.draw.rect(screen, self._gridColor, pg.Rect(outerX, outerY, outerW, outerH),  2) 

        # Draw the grid
        for row in range(self.rows):
            for col in range(self.cols):
                x = outerX + col * self._cellDims
                y = outerY + row * self._cellDims
                pg.draw.rect(screen, self._gridColor, pg.Rect(x, y, self._cellDims, self._cellDims),  2) 

        # draw the side wings of the board
        for row in range(self.rows):
            x = outerX - 3 * self._cellDims
            y = outerY + row * self._cellDims
            w = self._cellDims * 3
            h = self._cellDims
            pg.draw.rect(screen, self._gridColor, pg.Rect(x, y, w, h),  2) 

        # draw the top wings of the board
        for col in range(self.cols):
            y = outerY - 3 * self._cellDims
            x = outerX + col * self._cellDims
            h = self._cellDims * 3
            w = self._cellDims
            pg.draw.rect(screen, self._gridColor, pg.Rect(x, y, w, h),  2) 

    def update(self, keys):
        pass

class Game(object):
    def __init__(self) -> None:
        # initialize the pygame module
        pg.init()
        pg.display.set_caption("HRI Study")

        # create a fullscreen window for pygame to run
        self._screen = pg.display.set_mode((0, 0), pg.FULLSCREEN)

        # define a variable to control the main loop
        self._running = True

        self._keys = pg.key.get_pressed()

        self._nonogram = Nonogram()

    def event_loop(self):
        for event in pg.event.get():
            self._keys = pg.key.get_pressed()
            if event.type == pg.QUIT or self._keys[pg.K_ESCAPE]:
                self._running = False

    def draw(self):
        self._screen.fill(pg.Color("white"))
        self._nonogram.draw(screen=self._screen)

    def update(self):
        self._nonogram.update(keys=self._keys)

    def main_loop(self) -> None:
        # main loop
        while self._running:
            self.event_loop()
            self.update()
            self.draw()
            pg.display.update()
 
# define a main function
def main():
     game = Game()
     game.main_loop()
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()