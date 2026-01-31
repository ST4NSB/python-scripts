import cv2
import re
import streamlink
import easyocr
from win10toast_click import ToastNotifier
import webbrowser
import time
from colorama import Fore, Style, init
import datetime

# -- Twitch stream URL

url = "https://www.twitch.tv/forsen"

# -- User controls

notify_from_minute = 6 # Notifies the user when the in-game time is equal to or greater than this value
notify_until_including_minute = 16 # Notifies the user when the in-game time is equal to or less than this value

# -- Debug controls

show_debug_text = True
show_debug_video = False

# -- Notification controls

show_notification = True # True
wait_time_before_sending_notifications_in_seconds = 40

# -- Others

results_to_count = 3
confidence_threshold = 0.45

# -----------------------------

skip_frames = 175
max_ocr_checks = results_to_count
notif_duration_seconds = 30

init(autoreset=True)
stream = streamlink.streams(url)
if not stream:
    raise ValueError(f"The stream '{url}' is not LIVE or AVAILABLE")

stream_url = stream['best'].to_url()
reader = easyocr.Reader(lang_list=['en'], gpu=True, )
notif_sent = False
confirmed_mins = []

while True:
    if notif_sent:
        if show_debug_text:
            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Sleeping: {wait_time_before_sending_notifications_in_seconds} seconds.")
        time.sleep(wait_time_before_sending_notifications_in_seconds)
        notif_sent = False
    
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        raise ValueError("Could not open stream")
    
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    
    # captures 'IGT' tag and minutes and seconds only, ex. => IGT: 01:45
    region_width = 200
    x_offset = 112
    top_right_x = frame_width - region_width - x_offset
    region_height = 45
    top_right_y = 86
   
    passed_frames = 0
    ocr_checks_made = 0
   
    exit_check = False
    enable_ocr = False
    
    while exit_check is False:
        if passed_frames >= skip_frames:
            enable_ocr = True
       
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
        
        if show_debug_video:
            cv2.imshow("Twitch Stream", image)
        
        if enable_ocr:
            if ocr_checks_made >= max_ocr_checks:
                exit_check = True
            
            ocr_res = reader.readtext(image)
            if ocr_res:
                text = ocr_res[0][1]
                confidence = ocr_res[0][2]
                       
                if show_debug_text:
                    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Detected text: '{text}', confidence: '{confidence}'")
                
                patterns = ['IGT', 'IOT', 'IOI', 'IOM', 'IGI', 'IG1', '1O1', 'IT', 'TGT', "IOH", "IO1", "IGM"]
                igt_number_recognized = ('161', '101')
                text = text.replace(" ", "").replace("'", "").replace("`", "")
                text = text.upper()

                if any([x in text for x in patterns]) or text.startswith(igt_number_recognized):
                    if text.startswith(igt_number_recognized):
                        text = text[3:]

                    for word in patterns:
                        text = text.replace(word, "")
                    
                    digits_only = re.sub(r'\D', '', text)
                    
                    if len(digits_only) == 4:
                        minutes = digits_only[:2]
                        seconds = digits_only[2:4]
                        notif_message = f"forsen mc in-game time is: {minutes}:{seconds}"
                        
                        if show_debug_text: 
                            print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] {notif_message}, confirmed results minutes: {confirmed_mins[-results_to_count:]}")
                        if int(minutes) >= notify_from_minute and int(minutes) <= notify_until_including_minute:
                            if confidence < confidence_threshold:
                                if show_debug_text:
                                    print(Fore.YELLOW + f"Low confidence ({confidence}) for detected time '{minutes}:{seconds}'. Notification not sent." + Style.RESET_ALL)
                                continue
                            else:
                                confirmed_mins.append(int(minutes))
                            
                            confirmed_last_results = confirmed_mins[-results_to_count:]
                            if len(confirmed_last_results) < results_to_count:
                                continue

                            if show_notification and all(x == int(minutes) for x in confirmed_last_results):
                                confirmed_mins = []
                                if show_debug_text:
                                    print(Fore.RED + f"{notif_message.upper()}" + Style.RESET_ALL)
                                    
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