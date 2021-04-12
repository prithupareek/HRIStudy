from mistyPy import Robot
import random
from nonogram import EMPTY, SELECTED, CROSSED
import simpleaudio as sa
from multiprocessing import Process
from mutagen.wave import WAVE
import time

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
    def __init__(self, ip, condition):

        self.condition = condition

        # used to store the audioplaying process so the the nonogram can display the diagram while running
        self.p = None

        # Map from advice numbers to audio file names
        self.adviceAudioMap = {
                            NUMBER_EQ_GRIDSIZE: "1.wav",
                            OVERLAPPING: "2.wav",
                            NUM_SEP_BY_1: "3.wav",
                            UNREACHABLE: "4.wav",
                            STILL_SPACE: "5.wav",
                            MAKE_COMPLETE: "6.wav",
                            MERGE_AND_SPLIT: "7.wav",
                            DISTINGUISH_COMPLETE_GROUPS: "8.wav",
                            CONTRADICTION: "9.wav"
                        }
        self.adviceDiagramMap = {
                            NUMBER_EQ_GRIDSIZE: "Study_Advice_Diagrams/Slide1.png",
                            OVERLAPPING: "Study_Advice_Diagrams/Slide2.png",
                            NUM_SEP_BY_1: "Study_Advice_Diagrams/Slide3.png",
                            UNREACHABLE: "Study_Advice_Diagrams/Slide4.png",
                            STILL_SPACE: "Study_Advice_Diagrams/Slide5.png",
                            MAKE_COMPLETE: "Study_Advice_Diagrams/Slide6.png",
                            MERGE_AND_SPLIT: "Study_Advice_Diagrams/Slide7.png",
                            DISTINGUISH_COMPLETE_GROUPS: "Study_Advice_Diagrams/Slide8.png",
                            CONTRADICTION: "Study_Advice_Diagrams/Slide9.png"
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
                        
        if self.condition == "robot" or self.condition == "video":
            self.misty = Robot(ip)

            # for audio in self.adviceAudioMap:
            #     self.misty.uploadAudio("audio/" + self.adviceAudioMap[audio])

    def playAudio(self, wavefile):
        wave_obj = sa.WaveObject.from_wave_file(wavefile)
        play_obj = wave_obj.play()
        play_obj.wait_done()

    def noAudioDelay(self, wavefile):
        # delay for 15 seconds
        time.sleep(WAVE(wavefile).info.length)

    def playMistyAudio(self, wavefile):
        self.misty.playAudio(wavefile)
        time.sleep(WAVE(wavefile).info.length + 2)
        
    def giveAdvice(self, nonogram):
        bestAdvice = self.getBestAdvice(nonogram)
        print(bestAdvice)
        self.usedAdvice[bestAdvice] = True

        # get the filenames
        filename = "audio/" + self.adviceAudioMap[bestAdvice]
        diagramFilename = "assets/" + self.adviceDiagramMap[bestAdvice]
        duration = WAVE(filename).info.length

        # if in the video, robot, or debug conditions
        if self.condition == "video" or self.condition == "debug":
            function = self.playAudio            
        elif self.condition == "norobot":
            # create a new delay and show the diagram
            function = self.noAudioDelay
        elif self.condition == "robot":
            function = self.playMistyAudio

        self.p = Process(target=function, args=(filename,))
        self.p.start()

        return duration, diagramFilename


    
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
        for i in range(len(nonogram.puzzle)):
            if sum(nonogram.puzzle[i]) + len([a for a in nonogram.puzzle[i] if a != 0]) - 1 == nonogram.rows:
                if i < nonogram.cols:
                    if EMPTY in [nonogram.gameState[r][i] for r in range(nonogram.rows)]:
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
            col = [nonogram.gameState[r][c] for r in range(nonogram.rows)]
            solCol = [nonogram.solutionState[r][c] for r in range(nonogram.cols)]
            for r in range(nonogram.rows):
                if solCol[r] == SELECTED:
                    if col[r] != SELECTED:
                        break
                    if col[r] == SELECTED:
                        if EMPTY in col[:r] and EMPTY in col[r+1:]:
                            return True
        return False

    def check_still_space(self, nonogram):
        for row in range(nonogram.rows):
            puzzle = nonogram.puzzle[nonogram.rows + row]
            maxStretch = max(puzzle)
            currCount = 0
            counting = True
            for col in range(nonogram.cols):
                if nonogram.gameState[row][col] == SELECTED:
                    counting = False
                    currCount = 0
                if nonogram.gameState[row][col] == EMPTY:
                    if counting:
                        currCount += 1
                    else: 
                        continue
                if nonogram.gameState[row][col] == CROSSED:
                    if not counting:
                        counting = True
                        continue
                    else:
                        if currCount <= maxStretch and currCount != 0:
                            return True
                        currCount = 0
        
        for col in range(nonogram.cols):
            puzzle = nonogram.puzzle[col]
            maxStrech = max(puzzle)
            currCount = 0
            counting = True
            for row in range(nonogram.rows):
                if nonogram.gameState[row][col] == SELECTED:
                    counting = False
                    currCount = 0
                if nonogram.gameState[row][col] == EMPTY:
                    if counting:
                        currCount += 1
                    else: 
                        continue
                if nonogram.gameState[row][col] == CROSSED:
                    if not counting:
                        counting = True
                        continue
                    else:
                        if currCount <= maxStretch and currCount != 0:
                            return True
                        currCount = 0
        return False
                    




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
        # Randomly generate heuristic - only when more than 1/3 placed
        if random.randint(0, 99) > 90 and nonogram.getPlacedCount() >= int(nonogram.rows*nonogram.cols/3):
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
