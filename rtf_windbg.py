import subprocess
import os 
import shutil
from datetime import datetime
import threading 

timer = None

class CDBFuzzer(object):

    def __init__(self, programPath, crashDirectory, debuggerPath):
        self.programPath = programPath
        self.crashDirectory = crashDirectory
        self.debuggerPath = debuggerPath

    def killCdb(self, process):
        global timer
        try: process.terminate()
        except: pass
        try: timer.cancel()
        except: pass
    
    def startFuzz(self, inputFile, timeout):
        global timer

        commandLine = "\"" + self.debuggerPath + "\"" + ' ' + '-c ".logopen ' + self.crashDirectory + 'temp.log;g;.logclose ' + self.crashDirectory + 'temp.log" ' + "\"" + self.programPath + "\"" + ' ' + inputFile               
        self.process = subprocess.Popen(commandLine)
        
        timer = threading.Timer(timeout, self.killCdb, [self.process])
        timer.start()
        self.process.wait()
        try: timer.cancel()
        except: pass

    def stopFuzz(self):
        try:
            self.process.terminate()
        except:
            pass 

    def wasCrash(self):
        log = open(self.crashDirectory + 'temp.log').read()
        if "Access violation - code" in log:
            return True 

    def dumpCrash(self, crashName):
        shutil.copyfile(crashName, self.crashDirectory + crashName + "_" + datetime.now().strftime("%y-%m-%d-%H-%M") + ".log")
        shutil.copyfile("temp.log", self.crashDirectory + crashName + "_" + datetime.now().strftime("%y-%m-%d-%H-%M") + ".log")
