import cv2
import numpy as np
from threading import Timer



def process():
    global canProcess
    canProcess = True
            
    

cap = cv2.VideoCapture("\\Streams\\twitch\\live.mp4", cv2.CAP_FFMPEG) 


if (cap.isOpened() == False): 
    print("Error opening video stream or file") 
else: 
    print("NO opening errors! Good to go!")
    
    
t = Timer(20, process) # skip 20 seconds of commercial break 


started = False
canProcess = False
while (cap.isOpened()): 

    ret, frame = cap.read() 
    if ret == True: 
        if started is False:
            t.start()
            started = True
            
            
        #fr1 = frame[280:420, 1100:1280] # 720p60 = (720×1280, 3 colors)
        #fr1 = frame[280:300, 1100:1280] # 720p60 = (720×1280, 3 colors)
        fr1 = frame
        
        if canProcess is True:
            print(np.median(fr1))
            
        
        
        cv2.imshow('Frame', fr1)
        
            
        if cv2.waitKey(25) & 0xFF == ord('p'): 
            break 
             
print("Closing opencv stream processing!")
cap.release() # Closes all the frames 
cv2.destroyAllWindows()

    