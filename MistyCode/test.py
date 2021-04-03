from mistyPy import Robot
import time

misty = Robot("192.168.2.216")
misty.changeLED(0, 255, 255)
# misty.moveHeadPosition(0, 0, 0, 100) # center the head
# misty.moveArmsDegrees(0, 0, 100, 100)
# misty.moveHeadPosition(-5, 0, 0, 100) # center the head
# for i in range(10):
#     if i % 2 == 0:
#         misty.moveHeadPosition(0, 0, -5, 100) # center the head
#     else:
#         misty.moveHeadPosition(0, 0, 5, 100) # center the head
#     time.sleep(1)z

# misty.moveHeadPosition(0, 0, 0, 100) # center the head
# misty.changeLED(255, 0, 0)

# misty.printImageList()
misty.changeImage('e_SleepingZZZ.jpg')

# misty.uploadAudio("../audio/test.wav")
# misty.printAudioList()
for i in range(3):
    misty.playAudio('s_SleepySnore.wav')
    time.sleep(5)

