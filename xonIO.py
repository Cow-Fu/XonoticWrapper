from events import CmdEvent
from subprocess import Popen, PIPE
from threading import Thread
from datetime import timedelta
from time import sleep, time as currentTime
from collections import deque

class XonOutput(Thread):
    def __init__(self, process):
        Thread.__init__(self)
        self.collection = deque([])
        self.process = process

    def run(self):
        for line in outputStream(self.process):
            self.collection.append(line)

class XonInput(Thread):
    def __init__(self, process):
        Thread.__init__(self)
        self.cmds = []
        self.process = process

    @staticmethod
    def buildCmd(cmd, delay, flush=True):
        time = currentTime()
        return {
        "cmd": cmd,
        "time": time,
        "execTime": timedelta(seconds=time) + timedelta(seconds=delay),
        "flush": flush
        }

    def addCmd(self, cmd, delay, flush=True):
        self.cmds.append(self.buildCmd(cmd, delay, flush))

    def run(self):
        writer = writeToProcess(self.process)
        while not self.process.poll():
            time = timedelta(seconds=currentTime())
            c = list(filter(lambda cmd: time > cmd["execTime"], self.cmds))
            if c:
                for cmd in c:
                    writer(cmd["cmd"], flush=cmd["flush"])
                    self.cmds.remove(cmd)
            sleep(.1)

def startProcess(cmd):
    return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)

def startXonoticProcess():
    process = startProcess(_cmd)
    return (writeToProcess(process), process)

def outputStream(process):
    for line in process.stdout:
        yield line.strip()

def writeToProcess(process):
    def write(data, flush=True):
        if flush:
            data += "\n"
        process.stdin.write(data)
    return write

_cmd = "/home/nathan/xonoticgit/xonotic/all run sdl"
