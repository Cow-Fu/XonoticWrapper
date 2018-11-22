from subprocess import Popen, PIPE
from events import Event, DebugEvent, ChatMsgEvent, PlayerConnectEvent, FragEvent
from xonIO import startXonoticProcess, outputStream, XonInput, XonOutput
import PlayerManager
import re
from time import sleep


# regex = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")

# def outputStream():
#     lines = []
#     with open("outputVoid.txt", "rb") as f:
#         lines = f.read().decode("utf-8").split("\n")
#
#     for x in lines:
#         yield x

# writer, process = startXonoticProcess()

@ChatMsgEvent.connect
def moose(line, sender, message):
    if not sender == "Cow_Fu" and "moose" in message:
        writer('defer 1 "say why does everyone keep saying moose?"')

@FragEvent.connect
def lorax(victim, attacker, weapon, location, fragstreak):
    print("victim={}\nweapon={}".format(victim, weapon))
    if victim == "Cow_Fu" and (weapon == "Arc" or weapon == "Crylink"):
        streamWriter.addCmd('_cl_name ^xB70Lorax', -1)
        streamWriter.addCmd('say I am the Lorax, and I speak for the trees. The trees say: "can u fucking not?"', 1)
        streamWriter.addCmd('_cl_name Cow_Fu', 5.5)



# TODO: the following should probably be made into some type of event so we know when its init is complete
# and commands can be ran. Perhaps an echo should be ran after commands as well, so indicate they've finished
# writer("echo Xonwrapper init complete")
activeEvents = list(filter(lambda x: not x._exclude, Event.__subclasses__()))
passiveEvents = list(filter(lambda x: x._exclude, Event.__subclasses__()))

# writer, process = startXonoticProcess()
writer, process = startXonoticProcess()

streamWriter = XonInput(process)
streamReader = XonOutput(process)

streamWriter.setDaemon(True)
streamWriter.start()
streamReader.start()

while streamReader.isAlive():
    if streamReader.collection:
        line = streamReader.collection.popleft()
        if line == "":
            continue
        triggeredEvents = []
        for e in activeEvents:
            if e.check(line):
                triggeredEvents.append(e)

        if triggeredEvents:
            print("{}{}".format([line], triggeredEvents))
            for e in triggeredEvents:
                if getattr(e, "_cache"):
                    e.fire(**e._cache)
                else:
                    e.fire(line)
        else:
            print("{}{}".format(line, passiveEvents[1]))
    else:
        sleep(.05)
