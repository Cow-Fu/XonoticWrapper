from subprocess import Popen, PIPE
from blinker import signal

process = Popen(["/home/nathan/xonoticgit/xonotic/all run sdl"], shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True, bufsize=1)
for line in process.stdout:
    line = line.strip()
    if line == "execing config.cfg":
        print("Checking!")
        process.stdin.write("_cl_name\n")
    else:
        print(line)
