import numpy as np
import cv2
from mss import mss
import win32api
import winsound


cap = cv2.VideoCapture("\\Streams\\twitch\\recorded\\forsen\\forsen.mp4", cv2.CAP_FFMPEG) 

if (cap.isOpened() == False): 
    print("Error opening video stream or file") 
else: print("NO opening errors! Good to go!")

def show_info(can_show):
    if can_show:
        b_box = np.array(sct.grab(bounding_box_full))
        cv2.imshow('screen', b_box)

        print("Enter Nether: ", enter)
        print("Exit Nether: ", exit)
        print("Finding Stronghold: ", stronghold)
        print("World Record: ", worldr)
        print()


bounding_box_full = {'top': 389, 'left': 1337, 'width': 240, 'height': 87}
#timer= {'top': 480, 'left': 1370, 'width': 230, 'height': 50} # timer

enter_nether = {'top': 389, 'left': 1337, 'width': 240, 'height': 22}
exit_nether = {'top': 412, 'left': 1337, 'width': 240, 'height': 22}
finding_strong = {'top': 435, 'left': 1337, 'width': 240, 'height': 22}
world_rec = {'top': 457, 'left': 1337, 'width': 240, 'height': 22}


sct = mss()
threshold = 100
actual_position = ''
last_position = ''



while cap.isOpened():

    ret, frame = cap.read() 
    
    if ret == True: 

        enter = np.median(np.array(sct.grab(enter_nether)))
        exit = np.median(np.array(sct.grab(exit_nether)))
        stronghold = np.median(np.array(sct.grab(finding_strong)))
        worldr = np.median(np.array(sct.grab(world_rec)))

        show_info(can_show=True)

        if enter < threshold and exit < threshold and stronghold < threshold and worldr < threshold:
            last_position = actual_position
            actual_position = 'stopped speedrunning'

        if enter > threshold and exit < threshold and stronghold < threshold and worldr < threshold:
            last_position = actual_position
            actual_position = 'started a new game'
        if exit > threshold and enter < threshold and stronghold < threshold and worldr < threshold:
            last_position = actual_position
            actual_position = 'is in nether'
        if stronghold > threshold and enter < threshold and exit < threshold and worldr < threshold:
            last_position = actual_position
            actual_position = 'is looking for stronghold'
        if worldr > threshold and enter < threshold and exit < threshold and stronghold < threshold:
            last_position = actual_position
            actual_position = 'is fighting dragon'

        if actual_position is not last_position:
            print("Forsen ",actual_position.upper())
            #f actual_position == 'is in nether' or actual_position == 'stopped speedrunning':
            #    winsound.Beep(60, 800)
            if actual_position == 'is looking for stronghold':
                winsound.Beep(500, 800)
            if actual_position == 'is fighting dragon':
                winsound.Beep(1000, 800)
            #win32api.MessageBox(0, 'currently in: ' + actual_position.upper(), 'Forsen new position')

    if (cv2.waitKey(1) & 0xFF) == ord('p'):
        cv2.destroyAllWindows()
        break   