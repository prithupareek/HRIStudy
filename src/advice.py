# Advice numbers
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
import nonogram

class Advice():
    def __init__(self, ip):
        self.misty = Robot(ip)

        # TODO Create map from advice numbers to audio file names
        self.adviceAudioMap = {}
        self.usedAdvice = {
                            NUMBER_EQ_GRIDSIZE: False,
                            OVERLAPPING: False,
                            NUM_SEP_BY_1: False,
                            UNREACHABLE: False,
                            STILL_SPACE: False,
                            MAKE_COMPLETE: False,
                            MERGE_AND_SPLIT: False,
                            DISTINGUISH_COMPLETE_GROUPS: False,
                            CONTRADICTION: False
                        }
        
    def giveAdvice(self, nonogram):
        state = nonogram.gameState
        bestAdvice = self.getBestAdvice(state)
        self.usedAdvice[bestAdvice] = True
        # TODO: Look at board and back - Maybe threading?
        self.misty.playAudio(self.adviceAudioMap[bestAdvice])
    



    # TODO: Decide best advice
    def getBestAdvice(self, state):
        adviceList = self.list_of_advice(state)
        if adviceList == []:
            pass # TODO: pick one that hasn't been used
        return NUMBER_EQ_GRIDSIZE

    def check_num_eq_gridsize(self, nonogram):
        length = nonogram.rows
        solution = nonogram.solutionState

        # check the rows
        for row in range(length):
            if solution[row].count(1) == length:
                if nonogram.gameState[row].count(1) != length:
                    return True
            if solution[row].count(1) == 0:
                if nonogram.gameState[row].count(1) != 0:
                    return True

        for puzzle in nonogram.puzzle[:length]:
            if puzzle[2] != length:
                continue
            col = puzzle[2]
            for i in range(length):
                if nonogram.gameState[i][col] != 1:
                    return True
        return False

        

        
        

    # return list of advice that can be given given game state
    def list_of_advice(self, state):

        # check each advice and append it to the return list
        advice = list()
        if (check_num_eq_gridsize(gameState)):
            advice.append(NUMBER_EQ_GRIDSIZE)
        # TODO: Repeat for all possible advice
