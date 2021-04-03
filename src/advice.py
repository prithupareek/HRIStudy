from mistyPy import Robot
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
    def __init__(self, ip):
        # self.misty = Robot(ip) TODO: uncomment
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
        self.usedAdvice[bestAdvice] = True
        # TODO: Look at board and back - Maybe threading?
        self.misty.playAudio(self.adviceAudioMap[bestAdvice])
    
    # TODO: Decide best advice
    def getBestAdvice(self, nonogram):
        adviceList = self.list_of_advice(nonogram)
        if adviceList == []:
            pass # TODO: pick one that hasn't been used
        return NUMBER_EQ_GRIDSIZE #TODO: Fix this

    # TODO: Check if gridsize is applicable
    def check_num_eq_gridsize(self, nonogram):
        length = len(nonogram.gameState)
        for i in range(length):
            pass
    
    # TODO: Check if overlapping technique is applicable
    def check_overlapping(self, nonogram):
        pass

    # TODO: Check if separated by 1 is appicable
    def check_sep_by_1(self, nonogram):
        pass

    # TODO: Check if unreachable is applicable
    def check_unreachable(self, nonogram):
        pass

    # TODO: Check if still space is applicable
    def check_still_space(self, nonogram):
        pass

    # TODO: Check if make complete is applicable
    def check_make_complete(self, nonogram):
        pass

    # TODO: Check if merge split is applicable
    def check_merge_split(self, nonogram):
        pass
    
    # TODO: Check if distinguish complete groups is applicable
    def check_distinguish_groups(self, nonogram):
        pass

    # TODO: Check if contradiction is applicable
    def check_contradiction(self, nonogram):
        pass

    # return list of advice that can be given given game state
    def list_of_advice(self, nonogram):
        # check each advice and append it to the return list
        advice = list()
        for adv in range(LEN_ADVICE):
            if not self.usedAdvice[adv]:
                if self.adviceFunctions[adv](nonogram):
                    advice.append(adv)
        return advice
