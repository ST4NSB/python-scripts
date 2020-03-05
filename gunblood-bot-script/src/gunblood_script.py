import win32api, win32con
import time, msvcrt
import threading

def kbfunc():
    x = msvcrt.kbhit()
    if x:
        ret = msvcrt.getch()
    else:
        ret = False
    return ret

def move_to(x, y):
    win32api.SetCursorPos((x,y))

def move_and_click(x, y, repeatTimes = 1):
    win32api.SetCursorPos((x,y))
    for i in range(repeatTimes):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,x,y,0,0)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,x,y,0,0)

def play_func(wtime = 1.849999):
	t = threading.Timer(wtime, shoot_now)
	move_to(start_x, start_y)
	t.start()
    
def shoot_now():
	move_and_click(shoot_x, shoot_y)

#GunBlood y8 game
#screen bar open + 91%, semi screen on left side

start_x = 185
start_y = 620

shoot_x = 762
shoot_y = 378 

print("Script Initialized!")
print("Script Running!")

while True:
    #print(win32api.GetCursorPos())
    x = kbfunc()
    if x != False and (x.decode() == "o" or x.decode() == "O"):
        play_func(1.839555)
    if x != False and (x.decode() == "p" or x.decode() == "P"):
        play_func(1.849999)
    if x != False and (x.decode() == "s" or x.decode() == "S"):
        break

print("Script Stopped!")
