from events import CmdEvent
from subprocess import Popen, PIPE

def startProcess(cmd):
    return Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)

def outputStream(process):
    for line in process.stdout:
        yield line.strip()

def writeToProcess(process):
    def write(data, flush=True):
        if flush:
            data += "\n"
        process.stdin.write(data)
        CmdEvent._last_cmd = data
    return write

_cmd = "/home/nathan/xonoticgit/xonotic/all run sdl"

p = startProcess(_cmd)
write = writeToProcess(process=p)

write("echo Xonwrapper init complete")
for x in outputStream(p):
    print("Read: {}".format(x))
        # create a lock that transfers control over to another thingy

# p = startProcess(cmd)
