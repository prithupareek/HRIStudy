from mistyPy import Robot
import random
from nonogram import EMPTY, SELECTED, CROSSED

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
LEN_ADVICE = 9

class Advice():
    def __init__(self, ip):
        # self.misty = Robot(ip) TODO: uncomment later
        # TODO Create map from advice numbers to audio file names
        self.adviceAudioMap = {
                            NUMBER_EQ_GRIDSIZE: "",
                            OVERLAPPING: "",
                            NUM_SEP_BY_1: "",
                            UNREACHABLE: "",
                            STILL_SPACE: "",
                            MAKE_COMPLETE: "",
                            MERGE_AND_SPLIT: "",
                            DISTINGUISH_COMPLETE_GROUPS: "",
                            CONTRADICTION: ""
                        }
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
        self.adviceFunctions = {
                            NUMBER_EQ_GRIDSIZE: self.check_num_eq_gridsize,
                            OVERLAPPING: self.check_overlapping,
                            NUM_SEP_BY_1: self.check_sep_by_1,
                            UNREACHABLE: self.check_unreachable,
                            STILL_SPACE: self.check_still_space,
                            MAKE_COMPLETE: self.check_make_complete,
                            MERGE_AND_SPLIT: self.check_merge_split,
                            DISTINGUISH_COMPLETE_GROUPS: self.check_distinguish_groups,
                            CONTRADICTION: self.check_contradiction
                        }
        

    def giveAdvice(self, nonogram):
        bestAdvice = self.getBestAdvice(nonogram)
        print(bestAdvice)
        self.usedAdvice[bestAdvice] = True
        # TODO: Look at board and back - Maybe threading?
        # self.misty.playAudio(self.adviceAudioMap[bestAdvice]) TODO: uncomment later
    
    # Decide randomly from applicable/unused advice
    def getBestAdvice(self, nonogram):
        adviceList = self.list_of_advice(nonogram)
        if adviceList == []:
            # If none are applicable, get all of the unused advices
            adviceList = [advice for advice in self.usedAdvice if not self.usedAdvice[advice]]
        print(adviceList)
        return random.choice(adviceList)


    # Check if gridsize is applicable
    def check_num_eq_gridsize(self, nonogram):
        # TODO: Test
        length = nonogram.rows
        solution = nonogram.solutionState

        # check the rows
        for row in range(length):
            if solution[row].count(SELECTED) == length:
                if nonogram.gameState[row].count(SELECTED) != length:
                    return True
            if solution[row].count(SELECTED) == 0:
                if nonogram.gameState[row].count(SELECTED) != 0:
                    return True

        # Check the cols
        for puzzle in nonogram.puzzle[:length]:
            if puzzle[2] != length:
                continue
            col = puzzle[2]
            for i in range(length):
                if nonogram.gameState[i][col] != SELECTED:
                    return True
        return False

    
    # Check if overlapping technique is applicable
    def check_overlapping(self, nonogram):
        # iterate through each row and check if the puzzle is greater than half
        # of the length of the row:
        #   If it is, then check of the middle elements in the list is filled
        for row in range(nonogram.rows):
            puzzle = nonogram.puzzle[nonogram.rows + row]
            if puzzle[1] == 0:
                if puzzle[2] > nonogram.rows / 2:
                    gap = nonogram.rows - puzzle[2]
                    for j in range(gap, puzzle[2]):
                        if nonogram.gameState[row][j] != SELECTED:
                            return True

        # check columns
        for col in range(nonogram.cols):
            puzzle = nonogram.puzzle[col]
            if puzzle[1] == 0 and puzzle[2] > nonogram.cols / 2:
                gap = nonogram.cols - puzzle[2]
                for row in range(gap, puzzle[2]):
                    if nonogram.gameState[row][col] != SELECTED:
                        return True
        
        return False

    # Check if separated by 1 is appicable
    def check_sep_by_1(self, nonogram):
        # TODO: Test
        for i in nonogram.puzzle:
            if sum(nonogram.puzzle[i]) + len([a for a in nonogram.puzzle if a != 0]) - 1 == nonogram.rows:
                if i < nonogram.cols:
                    if EMPTY in [nonogram.gameState[r][i] for r in range(nonogram.row)]:
                        return True
                else:
                    row = i - nonogram.cols
                    if EMPTY in nonogram.gameState[row]:
                        return True
        return False

    # Check if unreachable is applicable
    def check_unreachable(self, nonogram):
        # TODO: Test
        # Check row to see if empty on either side of selected
        for r in range(nonogram.rows):
            row = nonogram.gameState[r]
            solRow = nonogram.solutionState[r]
            for c in range(nonogram.cols):
                if solRow[c] == SELECTED:
                    if row[c] != SELECTED:
                        break
                    if row[c] == SELECTED:
                        if EMPTY in row[:c] and EMPTY in row[c+1:]:
                            return True
        # Check col to see if empty on either side of selected
        for c in range(nonogram.cols):
            col = [nonogram.gameState[r][c] for r in range(nonograms.rows)]
            solCol = [nonogram.solutionState[r][c] for r in range(nonograms.cols)]
            for r in range(nonogram.rows):
                if solCol[r] == SELECTED:
                    if col[r] != SELECTED:
                        break
                    if col[r] == SELECTED:
                        if EMPTY in col[:r] and EMPTY in col[r+1:]:
                            return True
        return False

    # TODO: Check if still space is applicable
    def check_still_space(self, nonogram):
        pass

    # Check if make complete is applicable
    def check_make_complete(self, nonogram):
        # Check rows to see if empty between two selected in row
        for r in range(nonogram.rows):
            row = nonogram.gameState[r]
            if SELECTED in row:
                i1 = row.index(SELECTED)
                i2 = nonogram.rows - row[::-1].index(SELECTED) - 1
                if EMPTY in row[i1:i2]:
                    return True
        # Check cols to see if empty between two selected
        for c in range(nonogram.cols):
            col = [nonogram.gameState[r][c] for r in range(nonogram.rows)]
            if SELECTED in col:
                i1 = col.index(SELECTED)
                i2 = nonogram.cols - col[::-1].index(SELECTED) - 1
                if EMPTY in col[i1:i2]:
                    return True
        return False

    # Check if merge split is applicable
    def check_merge_split(self, nonogram):
        # TODO: Test
        # Randomly generate heuristic
        if random.randint(0, 99) > 90:
            return True
        return False
    
    def check_distinguish_groups(self, nonogram):
        # for every row, if they have the solution for the row, check if they 
        # crossed out every other cell
        for row in range(nonogram.rows):
            if nonogram.gameState[row].count(EMPTY) == 0:
                continue
            # check if row is correct, then return true
            isCorrect = True
            for col in range(nonogram.cols):
                if nonogram.solutionState[row][col] == CROSSED:
                    if (nonogram.gameState[row][col] == SELECTED):
                        isCorrect = False
                if nonogram.solutionState[row][col] == SELECTED:
                    if nonogram.gameState[row][col] != SELECTED:
                        isCorrect = False
            if isCorrect == True:
                return True 
        
        
        for col in range(nonogram.cols):
            # Check columns
            noCellEmpty = True 
            # check if any cell in column is empty
            for row in range(nonogram.rows):
                if nonogram.gameState[row][col] == EMPTY:
                    noCellEmpty = False
            
            if noCellEmpty:
                continue
            
            isCorrect = True
            for row in range(nonogram.rows):
                if nonogram.solutionState[row][col] == CROSSED:
                    if (nonogram.gameState[row][col] == SELECTED):
                        isCorrect = False
                if nonogram.solutionState[row][col] == SELECTED:
                    if nonogram.gameState[row][col] != SELECTED:
                        isCorrect = False
            if isCorrect == True:
                return True

        return False


    # Check if contradiction is applicable
    def check_contradiction(self, nonogram):
        # TODO: Test
        # Return true if participant incorrectly marked a square
        for row in range(nonogram.rows):
            for col in range(nonogram.cols):
                if nonogram.gameState[row][col] == SELECTED and nonogram.solutionState[row][col] == CROSSED:
                    return True
                if nonogram.gameState[row][col] == CROSSED and nonogram.solutionState[row][col] == SELECTED:
                    return True
        return False

    # return list of advice that can be given given game state
    def list_of_advice(self, nonogram):
        # check each advice and append it to the return list
        advice = list()
        for adv in range(LEN_ADVICE):
            if not self.usedAdvice[adv]:
                if self.adviceFunctions[adv](nonogram):
                    advice.append(adv)
        return advice
