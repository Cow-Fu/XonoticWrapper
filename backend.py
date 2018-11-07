from subprocess import Popen, PIPE
from events import Event
# import events
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
    with open("outputVoid.txt", "rb") as f:
        lines = f.read().decode("utf-8").split("\n")

    for x in lines:
        # if "\x1b[m:" in x and not regex.match(x):
        yield x

events = Event.__subclasses__()
# print(events)9
debug = events.pop()
_fragMsg = re.compile("^(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+.*'s (.*?) \(near (.*)\)(?:,[A-z\s]+(\d+))?|(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+).*?(\w+) \(near (.*)\))")
_suicideMsg = re.compile("^(?:\x1b\[\d\;\d+m)?(.*?)\x1b\[.{4}m(?!.*Shotgun)(?!.*'s).*? (\w+) \(near (.*?)\)")
# _suicideMsg = re.compile("^(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? (\w+) \(near (.*?)\)")
for line in outputStream():
    activeEvents = []
    for e in events:9
        if e.check(line):
            activeEvents.append(e)

    if activeEvents:
        for e in activeEvents:
            print(line, end="")
            print(e)
    else:
        print(line, end="")
        print(debug)
