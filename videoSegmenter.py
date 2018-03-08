#python3
import os
import re
import sys
import math
import time
import subprocess
from subprocess import run


class videoDurationProcess():
    """docstring for videoDurationProcess"""

    def __init__(self, filename):
        super(videoDurationProcess, self).__init__()
        self.filename = filename
        return

    def preprocess(self, filename):
        vfilename = self.filename
        logname = ""
        durtex = ""
        durtime = ""
        duration = 0
        parameter = "ffmpeg -i " + \
                    sys.path[0] + \
                    "/input/" + vfilename + " -report"
        run(parameter, shell=True)
        logexists = False
        logdir = os.listdir()
        print("Reading the information of video...")
        print("Current file: " + vfilename)
        while logexists == False:
            for logfile in logdir:
                extname = os.path.splitext(logfile)[1][1:]
                if extname == "log":
                    durfile = logfile
                    readlog = open(durfile, 'rb')
                    content = readlog.read().decode("utf-8")
                    readlog.close()
                    os.remove(logfile)
                    readdur = content[content.rfind("Duration:"):content.rfind("start") - 2]
                    print(readdur)
                    reg = "Duration\:\s(\d+)\:(\d+)\:([\d\.]+)"
                    durtime = re.compile(reg).findall(readdur)
                    print(durtime)
                    duration = int(durtime[0][0]) * 3600 + int(durtime[0][1]) * 60 + float(durtime[0][2])
                    print("Total time: " + str(duration))
                    logexists = True
                    return duration
                else:
                    time.sleep(1)


class videoCut():
    """docstring for videoCut"""

    def __init__(self, filename):
        super(videoCut, self).__init__()
        self.filename = filename
        return

    def process(self, filename, parttime):
        vfilename = self.filename
        extvname = os.path.splitext(self.filename)[1][1:]
        durtime = videoDurationProcess(vfilename).preprocess(vfilename)
        startat = 0
        print("Predicting the number of segmentation: " + str(math.ceil(int(durtime) / int(parttime))))
        print("-------------")
        for i in range(1, math.ceil(int(durtime) / int(parttime) + 1)):
            print("Segmenting " + str(i) + "th...")
            parameter = "ffmpeg -n -ss " + str(startat) + " -i input/" + vfilename + " -c copy -t " + \
                        str(parttime) + " output/" + self.filename + "_" + str(i) + "." + extvname
            run(parameter, shell=True)
            startat += parttime
        print("--------already finished: " + vfilename + "-------")
        return


if __name__ == "__main__":
    if not os.path.exists("input"):
        os.mkdir("input")
    if not os.path.exists("output"):
        os.mkdir("output")
    parttime = input("How long of the short video do you need:(second) ")
    # parttime = 300
    print("-------------")
    filesname = os.listdir("input")
    for filename in filesname:
        videoCut(filename).process(filename, int(parttime))
    print("done !!")
