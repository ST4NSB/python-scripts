import requests
import os
import time
import sys
import subprocess
import datetime
import getopt
import shutil

class TwitchRecorder:
    def __init__(self):
        # global configuration
        self.client_id = "gp762nuuoqcoxypju8c569th9wz7q5"  # don't change this
        # get oauth token value by typing `streamlink --twitch-oauth-authenticate` in terminal
        self.oauth_token = "9gbk1aw3vljm8l4ez8wdf57psjrm2f"
        self.ffmpeg_path = 'D:/Programs/ffmpeg/bin/ffmpeg.exe'
        self.refresh = 60.0
        self.root_path = "\\Streams\\twitch"

        # user configuration
        self.username = "squillakilla"
        self.user_id = '61855433'
        self.quality = "720p60"

        # path to recorded stream
        self.recorded_path = self.root_path

    def run(self):
        # path to finished video, errors removed

        # create directory for recordedPath and processedPath if not exist
        if (os.path.isdir(self.recorded_path) is False):
            os.makedirs(self.recorded_path)

        # make sure the interval to check user availability is not less than 15 seconds
        if (self.refresh < 15):
            print("Check interval should not be lower than 15 seconds.")
            self.refresh = 15
            print("System set check interval to 15 seconds.")

        # fix videos from previous recording session
        '''
        try:
            video_list = [f for f in os.listdir(self.recorded_path) if
                          os.path.isfile(os.path.join(self.recorded_path, f))]
            if (len(video_list) > 0):
                print('Fixing previously recorded files.')
            for f in video_list:
                recorded_filename = os.path.join(self.recorded_path, f)
                print('Fixing ' + recorded_filename + '.')
                try:
                    subprocess.call(
                        [self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy',
                         os.path.join(self.processed_path, f)])
                    os.remove(recorded_filename)
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)
        '''

        print("Checking for", self.username, "every", self.refresh, "seconds. Record with", self.quality, "quality.")
        self.loopcheck()

    def check_user(self):
        # 0: online,
        # 1: offline,
        # 2: not found,
        # 3: error
        url = 'https://api.twitch.tv/helix/streams?user_id=' + self.user_id
        info = None
        status = 3
        try:
            r = requests.get(url,  headers={"Client-ID": self.client_id, "Authorization": "Bearer " + self.oauth_token}, timeout=15)
            r.raise_for_status()
            info = r.json()
            if info['data'][0].get("type") is None: # dictionary check problem here
                status = 1
            else:
                status = 0
        except requests.exceptions.RequestException as e:
            if e.response:
                if e.response.reason == 'Not Found' or e.response.reason == 'Unprocessable Entity':
                    status = 2

        return status, info

    def loopcheck(self):
        while True:
            status, info = self.check_user()
            if status == 2:
                print("Username not found. Invalid username or typo.")
                time.sleep(self.refresh)
            elif status == 3:
                print(datetime.datetime.now().strftime("%Hh%Mm%Ss"), " ",
                      "unexpected error. will try again in 5 minutes.")
                time.sleep(300)
            elif status == 1:
                print(self.username, "currently offline, checking again in", self.refresh, "seconds.")
                time.sleep(self.refresh)
            elif status == 0:
                print(self.username, "online. Stream recording in session.")
                filename = "live.mp4"

                # clean filename from unecessary characters
                filename = "".join(x for x in filename if x.isalnum() or x in [" ", "-", "_", "."])

                recorded_filename = os.path.join(self.recorded_path, filename)

                # start streamlink process
                subprocess.call(
                    ["streamlink", "--twitch-oauth-token", self.oauth_token, "twitch.tv/" + self.username, self.quality,
                     "-o", recorded_filename])

                print("Recording stream is done. Fixing video file.")
                if (os.path.exists(recorded_filename) is True):
                    try:
                        subprocess.call(
                            [self.ffmpeg_path, '-err_detect', 'ignore_err', '-i', recorded_filename, '-c', 'copy',
                             os.path.join(self.processed_path, filename)])
                        os.remove(recorded_filename)
                    except Exception as e:
                        print(e)
                else:
                    print("Skip fixing. File not found.")

                print("Fixing is done. Going back to checking..")
                time.sleep(self.refresh)


def process_stream(argv):
    usage_message = 'twitch-recorder.py -u <username> -q <quality>'

    try:
        opts, args = getopt.getopt(argv, "hu:q:", ["username=", "quality="])
    except getopt.GetoptError:
        print(usage_message)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage_message)
            sys.exit()
        elif opt in ("-u", "--username"):
            twitch_recorder.username = arg
        elif opt in ("-q", "--quality"):
            twitch_recorder.quality = arg

if __name__ == "__main__":
    shutil.rmtree('/Streams', ignore_errors=True)
    twitch_recorder = TwitchRecorder()
    process_stream(sys.argv[1:])
    twitch_recorder.run()
