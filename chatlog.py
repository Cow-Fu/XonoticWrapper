import re
from events import Events

_MAX_LOG_SIZE = 1000
_chat_log = []
_extractMsg = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")

class ChatMsg(Event):
    @classmethod
    def check(cls, line):
        return True if _extractMsg.findall(line) else False

@ChatMsg.connect
def addMsg(sender, contents, line):
    _chat_log.append({"sender": sender, "contents": contents, "fullLine": line})
    _cleanup()

def _cleanup():
    while len(_chat_log) > _MAX_LOG_SIZE:
        del _chat_log[-1]
def extractInfo(line):
    matches = _extractMsg.match(line)
    if matches:
        return tuple(matches.groups() + line)
    else:
        return None
