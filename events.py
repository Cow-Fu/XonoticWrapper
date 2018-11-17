
import re

from abc import ABC, abstractmethod

# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]

class Event(ABC):
    _exclude = False
    _has_handler = False

    @classmethod
    def addHandler(cls, func):
        cls._handlers.append(func)

    @classmethod
    def removeHandler(cls, func):
        cls._handlers.remove(func)

    @classmethod
    def getEventHandlers(cls):
        return cls._handlers

    @classmethod
    def connect(cls, func):
        def wrapper(*args, **kwargs):
            func(*args, **kwargs)
        cls.addHandler(func)
        return wrapper

    @abstractmethod
    def check(*args, **kwargs):
        pass

    @classmethod
    def fire(cls, *args, **kwargs):
        for func in cls._handlers:
            func(*args, **kwargs)

class PlayerConnectingEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            cls._cache["name"] = line[line.index(" is connecting...")]
            return True
        except ValueError:
            cls._cache = {}
            return False

class PlayerConnectEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            cls._cache["name"] = line[line.index(" connected\x1b[m")]
            return True
        except ValueError:
            cls._cache = {}
            return False

class PlayerSpectateEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            cls._cache["name"] = line[line.index(" is now spectating\x1b[m")]
            return True
        except ValueError:
            cls._cache = {}
            return False

class PlayerJoinEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            cls._cache["name"] = line[line.index(" is now playing\x1b[m")]
            return True
        except ValueError:
            cls._cache = {}
            return False

class PlayerDisconnectEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            cls._cache["name"] = line[line.index(" disconnected\x1b[m")]
            return True
        except ValueError:
            cls._cache = {}
            return False


class ChatMsgEvent(Event):
    _chatMsg = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")
    @classmethod
    def check(cls, line):
        temp = cls._chatMsg.match(line)
        if temp:
            cls._cache["line"] = temp[0]
            cls._cache["sender"] = temp[1]
            cls._cache["message"] = temp[2]
            return True
        else:
            cls._cache = {}
        return False

class FragEvent(Event):
    _fragMsg = re.compile("^(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+.*'s (.*?) \(near (.*)\)(?:,[A-z\s]+(\d+))?|(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+).*?(\w+) \(near (.*)\))")
    @classmethod
    def check(cls, line):
        temp = cls._fragMsg.match(line)
        if temp:
            temp = tuple(filter(lambda x: x, temp.groups()))
            cls._cache["line"] = temp[0]
            cls._cache["victim"] = temp[1]
            cls._cache["attacker"] = temp[2]
            cls._cache["weapon"] = temp[3]
            cls._cache["location"] = temp[4]
            try:
                cls._cache["fragstreak"] = temp[5]
            except IndexError:
                cls._cache["fragstreak"] = None
            finally:
                return True
        else:
            cls._cache = {}
        return False

class SuicideEvent(Event):
    _suicideMsg = re.compile("^(?:\x1b\[\d\;\d+m)?(.*?)\x1b\[.{4}m(?!.*Shotgun)(?!.*'s).*? (\w+) \(near (.*?)\)")

    @classmethod
    def check(cls, line):
        return True if cls._suicideMsg.match(line) else False

class CmdEvent(Event):
    _exclude = True
    _last_cmd = None

    @classmethod
    def check(cls, line):
        return cls._last_cmd == line

class DebugEvent(Event):
    _exclude = True
    @classmethod
    def check(cls, line):
        return True

for c in Event.__subclasses__():
    print(c)
    setattr(c, "_handlers", [])
    setattr(c, "_cache", {})
