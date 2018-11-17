from events import CmdEvent
from subprocess import Popen, PIPE
from threading import Thread

class XonIO(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.collection = deque([])

    def run(self, process):
        for line in process:
            self.collection.append(line)

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
