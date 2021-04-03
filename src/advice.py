
NUMBER_EQ_GRIDSIZE = 0 
OVERLAPPING = 1
NUM_SEP_BY_1 = 2
UNREACHABLE = 3
STILL_SPACE = 4
MAKE_COMPLETE = 5
MERGE_AND_SPLIT = 6
DISTINGUISH_COMPLETE_GROUPS = 7
CONTRADICTION = 8

from mistyPy import Robot
import time

class Advice():
    def __init__(self, ip):
        self.misty = Robot(ip)


    def giveAdvice(self, nonogram):
        state = nonogram.gameState
        return 0
    
    def check_num_eq_gridsize(self):
        length = len(self.gameState)
        for i in range(length):
        pass
        
        # return list of advice that can be given given game state
    def list_of_advice():
        # check each advice and append it to the return list
        advice = list()
        if (check_num_eq_gridsize(gameState)):
            advice.append(NUMBER_EQ_GRIDSIZE)
