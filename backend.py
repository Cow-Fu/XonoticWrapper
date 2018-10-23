from subprocess import Popen, PIPE
from events import Events
import PlayerManager

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
    with open("output2.txt", "rb") as f:
        lines = f.read().decode("utf-8").split("\n")
    for x in lines:
        if "connected" in x and "ahh" in x:
            yield x

for line in outputStream():
#     if "MQC Build information:" in line:
#         initMsgs = True
#
#     if not initMsgs:
#         continue
#
    if line.endswith(" connected\x1b[m"):
        Events.PLAYER_CONNECTED.send(line[:line.index(" connected\x1b[m")])
    elif line.endswith(" is now spectating\x1b[m"):
        Events.PLAYER_SPECTATE.send(line[:line.index(" is now spectating\x1b[m")])
    # TODO: ctf message is like "is now playing on the RED/BLUE team"
    elif line.endswith(" is now playing\x1b[m"):
        Events.PLAYER_JOIN.send(line[:line.index(" is now playing\x1b[m")])
    elif line.endswith(" disconnected\x1b[m"):
        Events.PLAYER_DISCONNECT.send(line[:line.index(" disconnected\x1b[m")])
    print(line)
    print([line])
    # print([x for x in line])

for k, v in PlayerManager.getPlayers().items():
    pass
    # print("{}: {}".format(k, v))
    # print(repr(player))
