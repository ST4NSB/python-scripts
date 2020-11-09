import numpy as np
import cv2
from mss import mss
import win32api
import winsound


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
#bounding_box = {'top': 480, 'left': 1370, 'width': 230, 'height': 50} # timer

enter_nether = {'top': 389, 'left': 1337, 'width': 240, 'height': 22}
exit_nether = {'top': 412, 'left': 1337, 'width': 240, 'height': 22}
finding_strong = {'top': 435, 'left': 1337, 'width': 240, 'height': 22}
world_rec = {'top': 457, 'left': 1337, 'width': 240, 'height': 22}


sct = mss()
threshold = 100
actual_position = ''
last_position = ''

while True:

    enter = np.median(np.array(sct.grab(enter_nether)))
    exit = np.median(np.array(sct.grab(exit_nether)))
    stronghold = np.median(np.array(sct.grab(finding_strong)))
    worldr = np.median(np.array(sct.grab(world_rec)))

    show_info(can_show=False)

    if enter < threshold and exit < threshold and stronghold < threshold and worldr < threshold:
        last_position = actual_position
        actual_position = 'not speedrunning'

    if enter > threshold and exit < threshold and stronghold < threshold and worldr < threshold:
        last_position = actual_position
        actual_position = 'enter nether'
    if exit > threshold and enter < threshold and stronghold < threshold and worldr < threshold:
        last_position = actual_position
        actual_position = 'exit nether'
    if stronghold > threshold and enter < threshold and exit < threshold and worldr < threshold:
        last_position = actual_position
        actual_position = 'finding stronghold'
    if worldr > threshold and enter < threshold and exit < threshold and stronghold < threshold:
        last_position = actual_position
        actual_position = 'world record!'

    if actual_position is not last_position:
        print("Forsen position: ",actual_position.upper())
        if actual_position == 'exit nether' or actual_position == 'not speedrunning':
            winsound.Beep(80, 800)
        if actual_position == 'finding stronghold':
            winsound.Beep(500, 800)
        if actual_position == 'world record':
            winsound.Beep(1000, 800)
        #win32api.MessageBox(0, 'currently in: ' + actual_position.upper(), 'Forsen new position')

    if (cv2.waitKey(1) & 0xFF) == ord('p'):
        cv2.destroyAllWindows()
        break