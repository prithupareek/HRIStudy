from mistyPy import Robot
import time

class Advice():
    def __init__(self, ip):
        self.misty = Robot(ip)
        
    def giveAdvice(self, nonogram):
        state = nonogram.gameState
        return 0

