import cv2
import numpy as np

cap = cv2.VideoCapture("\\Streams\\twitch\\live.mp4", cv2.CAP_FFMPEG) 


if (cap.isOpened() == False): 
    print("Error opening video stream or file") 
else: print("NO opening errors! Good to go!")
    
while (cap.isOpened()): 
    # Capture frame-by-frame 
    ret, frame = cap.read() 
    if ret == True: 
    
        fr1 = frame[450:650, 700:1000] # 720p60 = (1080×1920, 3 colors)
        #fr1 = frame
        
        
        
        cv2.imshow('Frame', fr1)
        
        if cv2.waitKey(25) & 0xFF == ord('p'): 
            break 
    #else: 
    #    break 
        
        
        
print("Closing!")
cap.release() # Closes all the frames 
cv2.destroyAllWindows()
    
    