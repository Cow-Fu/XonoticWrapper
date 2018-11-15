from subprocess import Popen, PIPE
from events import Event, DebugEvent, ChatMsgEvent
from xonIO import startXonoticProcess, outputStream
import PlayerManager
import re

# regex = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")

# def outputStream():
#     lines = []
#     with open("outputCmd.txt", "rb") as f:
#         lines = f.read().decode("utf-8").split("\n")
#
#     for x in lines:
#         yield x
# writer, process = startXonoticProcess()
activeEvents = list(filter(lambda x: not x._exclude, Event.__subclasses__()))
passiveEvents = list(filter(lambda x: x._exclude, Event.__subclasses__()))

print(activeEvents)
print(passiveEvents)
exit()


for line in outputStream(process):
    if line == "":
        continue
    triggeredEvents = []
    for e in events:
        if e.check(line):
            triggeredEvents.append(e)

    if triggeredEvents:
        for e in triggeredEvents:
            print(e)
            e.fire(line)
            print("{}{}".format(line, e))
    else:
        print("{}{}".format(line, debug))
