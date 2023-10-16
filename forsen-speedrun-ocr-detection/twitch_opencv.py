import cv2
import re
import streamlink
import easyocr
from win10toast_click import ToastNotifier
import webbrowser
import time

# -- User controls

url = "https://www.twitch.tv/forsen" # forsen
notice_minutes = 10 # 10
notice_minutes_max_allowed = 17 # 17
wait_time_before_notifications_seconds = 60 * 1 # 60 * 1
show_debug_video = False # False
show_debug_image = False # False
show_debug_text = True # True

# -----------------

skip_frames = 440 # 440
max_ocr_checks = 15 # 15
notif_duration_seconds = 10 # 10

stream = streamlink.streams(url)
if not stream:
    raise ValueError(f"The stream '{url}' is not LIVE or AVAILABLE")

stream_url = stream['best'].to_url()
reader = easyocr.Reader(lang_list=['en'], gpu=True)
notif_sent = False

while True:
    if notif_sent:
        print(f"Sleeping: {wait_time_before_notifications_seconds} seconds.")
        time.sleep(wait_time_before_notifications_seconds)
        notif_sent = False
    
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise ValueError("Could not open stream")
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    region_width = 212
    region_height = 30
    top_right_x = frame_width - region_width - 28
    top_right_y = 79
   
    passed_frames = 0
    ocr_checks_made = 0
   
    exit_check = False
    enable_ocr = False
    
    while exit_check is False:
        if passed_frames >= skip_frames:
            enable_ocr = True
       
        if show_debug_image:
            image = cv2.imread('tess_photo_test.png') # test image
        else:
            ret, frame = cap.read()
            if not ret:
                raise ValueError("Could not read frame")
                
            image = frame[top_right_y:top_right_y + region_height, top_right_x:top_right_x + region_width]     
        
        # preprocessing
        try:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            ret, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            image = cv2.GaussianBlur(image, (5, 5), 0)
            image = cv2.convertScaleAbs(image, alpha=1.5, beta=50)
            desired_width = 800
            aspect_ratio = desired_width / image.shape[1]
            new_height = int(image.shape[0] * aspect_ratio)
            image = cv2.resize(image, (desired_width, new_height))
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        except:
            pass
        
        if enable_ocr:
            if ocr_checks_made >= max_ocr_checks:
                exit_check = True
            
            ocr_res = reader.readtext(image)
            if ocr_res:
                text = ocr_res[0][1]
                confidence = ocr_res[0][2]

                if show_debug_text:
                    print(f"Detected text: '{text}', confidence: '{confidence}'")
                
                patterns = ['IGT', 'IOT', 'IOI', 'IOM', 'IGI']
                igt_number_recognized = '161'
                if any([x in text.upper() for x in patterns]) or text.startswith(igt_number_recognized):
                    if text.startswith(igt_number_recognized):
                        text = text[3:]
                    digits_only = re.sub(r'\D', '', text)
                    
                    if len(digits_only) >= 4:
                        minutes = digits_only[:2]
                        seconds = digits_only[2:4]
                        notif_message = f"forsen mc in-game time is: {minutes}:{seconds}"
                        
                        if show_debug_text: 
                            print(notif_message)
                        if int(minutes) >= notice_minutes and int(minutes) <= notice_minutes_max_allowed:
                            toaster = ToastNotifier()
                            title = "forsen minecraft"
                            message = notif_message
                            
                            try:
                                toaster.show_toast(title, message, duration=notif_duration_seconds, callback_on_click=lambda: webbrowser.open_new(url))
                            except:
                                raise ValueError("Push window notification error")
                            
                            notif_sent = True
                            
                        exit_check = True
            
            ocr_checks_made += 1

        if show_debug_video:
            cv2.imshow("Twitch Stream", image)

        passed_frames += 1

        if show_debug_video:
            if cv2.waitKey(1) & 0xFF == ord('d'):
                enable_ocr = False
            if cv2.waitKey(1) & 0xFF == ord('e'):
                enable_ocr = True
    
    try:
        cap.release()
        if show_debug_video:
            cv2.destroyAllWindows()
    except:
        pass