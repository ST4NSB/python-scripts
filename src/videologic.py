
from moviepy.editor import VideoFileClip, concatenate_videoclips

class VideoLogic:
    def __init__(self):
        pass
    
    def setVideoPath(self, uploadedPath):
        self.path = uploadedPath
        self.outputFormat = "mp4"
    
    def getVideoPath(self):
        return self.path

    def isFormatAvailable(self, format):
        formats = {
            'mp4': True,
            'avi': True,
            'wav': True,
            'gif': True,
        }
        return formats.get(format, False)

    def getVideoFormat(self):
        vFormat = ""
        for i in range(len(self.getVideoPath()) - 1, 0, -1):
            if self.getVideoPath()[i] == '.':
                vFormat = self.getVideoPath()[i+1:]
        return vFormat

    def renameModifiedFile(self):
        vFormat = self.getVideoFormat()
        oldName = self.getVideoPath()
        name = ""
        for i in range(0, len(self.getVideoPath())):
            if oldName[i] != '.':
                name += oldName[i]
            else: break
        name += "_loop."
        name += self.outputFormat 
        return name
    
    def LoopClipMethod(self, numberOfTimes):
        video = clip = VideoFileClip(self.getVideoPath())
        # loop n times
        n = int(numberOfTimes)
        for i in range(n - 1):
            video = concatenate_videoclips([video,clip])
        newFile = self.renameModifiedFile()
        video.write_videofile(newFile)

    def LoopClipLength(self, hours, minutes, seconds):
        video = clip = VideoFileClip(self.getVideoPath())
        # loop based on time (hh:mm:ss)
        timeDurationWanted = int(seconds) + int(minutes)*60 + int(hours)*3600
        initialClipDuration = int(clip.duration)
        numberOfTimes = int(timeDurationWanted / initialClipDuration)
        subclipDuration = int(timeDurationWanted % initialClipDuration)
        print("The new video clip will have a length of ~", timeDurationWanted, "seconds: ", )
        for i in range(numberOfTimes - 1):
            video = concatenate_videoclips([video,clip])
        clip = VideoFileClip(self.getVideoPath()).subclip(0, subclipDuration)
        video = concatenate_videoclips([video,clip])
        newFile = self.renameModifiedFile()
        video.write_videofile(newFile)