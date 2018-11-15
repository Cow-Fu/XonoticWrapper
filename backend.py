from subprocess import Popen, PIPE
from events import Event, DebugEvent, ChatMsgEvent
import PlayerManager
import re

regex = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")

def startProcess(cmd):
    return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)

# def outputStream(process):
#     for line in process.stdout:
#         yield line.strip()

def writeToProcess(process):
    def write(data, flush=True):
        if flush:
            data += "\n"
        process.stdin.write(data)
    return write

cmd = "/home/nathan/xonoticgit/xonotic/all run sdl"
# p = startProcess(cmd)
# write = writeToProcess(process=p)

def outputStream():
    lines = []
    with open("outputCmd.txt", "rb") as f:
        lines = f.read().decode("utf-8").split("\n")

    for x in lines:
        yield x

events = Event.__subclasses__()
# for x in events:
#     if x._exclude == True:
#         print(x)
#         exit()
# events.remove(debug)
for x in events:
    if x is DebugEvent:
        debug = x
        break
events.remove(debug)

for line in outputStream():
    if line == "":
        continue
    activeEvents = []
    for e in events:
        if e.check(line):
            activeEvents.append(e)

    if activeEvents:
        for e in activeEvents:
            print(e)
            e.fire(line)
            print("{}{}".format(line, e))
    else:
        print("{}{}".format(line, debug))
