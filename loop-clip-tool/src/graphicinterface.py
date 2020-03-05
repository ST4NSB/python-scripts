
import tkinter as tk
from tkinter import filedialog
from videologic import *

class GraphicInterface:

    def __init__(self):
        print(tk.TkVersion)
        self.vidLogic = VideoLogic()
        self.windowTitle = "Loop a mp4 video .."
        self.labelFontInfo = "Arial 12"
        self.windowSize = "300x340+200+120"
        self.filename = ""
        self.createWindow()

    def eliminatePath(self):
        for i in range(len(self.filename) - 1, 0, -1):
            if self.filename[i] == '/':
                return self.filename[i+1:]
        return ""

    def UploadAction(self):
        self.filename = filedialog.askopenfilename()
        print("You uploaded:", self.eliminatePath())


    def ProceedFirstMethod(self):
        self.vidLogic.setVideoPath(self.filename)
        if not self.firstTxtBox.get().isdigit(): return print("ERROR: the number of loops is not an integer number!")
        if len(self.filename) is 0: return print("ERROR: video file not uploaded!")
        vFormat = self.vidLogic.getVideoFormat()
        print("Uploaded file format is: ", vFormat)
        if not self.vidLogic.isFormatAvailable(vFormat): return print("ERROR: format not available!")
        self.vidLogic.LoopClipMethod(self.firstTxtBox.get())


    def ProceedSecondMethod(self):
        self.vidLogic.setVideoPath(self.filename)     
        if not self.hoursTxtBox.get().isdigit(): return print("ERROR: the number of hours is not an integer number!")
        if not self.minutesTxtBox.get().isdigit(): return print("ERROR: the number of minutes is not an integer number!")
        if not self.secsTxtBox.get().isdigit():  return print("ERROR: the number of seconds is not an integer number!")
        if len(self.filename) is 0: return print("ERROR: video file not uploaded!") 
        vFormat = self.vidLogic.getVideoFormat()
        print("Uploaded file format is: ", vFormat)
        if not self.vidLogic.isFormatAvailable(vFormat): return print("ERROR: format not available!")  
        self.vidLogic.LoopClipLength(self.hoursTxtBox.get(), self.minutesTxtBox.get(), self.secsTxtBox.get())


    def addComponents(self):
        tk.Label(self.root, text='Select a file format (.mp4,.GIF,.avi,.wav)', font=self.labelFontInfo).grid(row=0, column=0, sticky=tk.W)
        tk.Label(self.root, text='Upload a file ', font=self.labelFontInfo).grid(row=1, column=0, sticky=tk.W)
        tk.Button(self.root, text="Browse ..", command=self.UploadAction).grid(row=1, column = 0,  padx=(100, 0),  sticky=tk.W)
        
        tk.Label(self.root, text='', font=self.labelFontInfo).grid(row=2, column=0, sticky=tk.W)
        tk.Label(self.root, text=" Method 1: Video looping the same clip", font=self.labelFontInfo).grid(row=3, sticky=tk.W)
        tk.Label(self.root, text="Set number of clip loops ", font=self.labelFontInfo).grid(row=4, column = 0, sticky=tk.W)
        self.firstTxtBox = tk.Entry(self.root, textvariable=tk.StringVar(self.root, value='2'), width=8)
        self.firstTxtBox.grid(row=5, column=0, sticky=tk.W, padx=(5, 0))
        tk.Button(self.root, text="Proceed Method 1", command=self.ProceedFirstMethod).grid(row=5, column = 0, padx=(60, 0), sticky=tk.W)
        
        tk.Label(self.root, text='', font=self.labelFontInfo).grid(row=6, column=0, sticky=tk.W)
        tk.Label(self.root, text=" Method 2: Set Video Length looping", font=self.labelFontInfo).grid(row=7, sticky=tk.W)
        tk.Label(self.root, text=" (looping the same clip for [hh:mm:ss])", font=self.labelFontInfo).grid(row=8, sticky=tk.W)
        tk.Label(self.root, text=" hours ", font=self.labelFontInfo).grid(row=9,column=0,padx=(60, 0), sticky=tk.W)
        self.hoursTxtBox = tk.Entry(self.root, textvariable=tk.StringVar(self.root, value='0'), width=8)
        self.hoursTxtBox.grid(row=9, column=0, padx=(5, 0), sticky=tk.W)
        tk.Label(self.root, text=" minutes ", font=self.labelFontInfo).grid(row=10,column=0, sticky=tk.W,padx=(60, 0))
        self.minutesTxtBox = tk.Entry(self.root, textvariable=tk.StringVar(self.root, value='0'), width=8)
        self.minutesTxtBox.grid(row=10, column=0, padx=(5, 0), sticky=tk.W)
        tk.Label(self.root, text=" seconds ", font=self.labelFontInfo).grid(row=11,column=0, sticky=tk.W,padx=(60, 0))
        self.secsTxtBox = tk.Entry(self.root, textvariable=tk.StringVar(self.root, value='20'), width=8)
        self.secsTxtBox.grid(row=11, column=0, padx=(5, 0), sticky=tk.W) 
        tk.Button(self.root, text="Proceed Method 2", command=self.ProceedSecondMethod).grid(row=12, column = 0, padx=(5,0), sticky=tk.W)

    def createWindow(self):
        self.root = tk.Tk()
        self.root.resizable(False, False)
        self.root.title(self.windowTitle)
        self.root.geometry(self.windowSize)
        self.addComponents()
        self.root.mainloop()

    