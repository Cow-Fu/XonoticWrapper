
import re

from abc import ABC, abstractmethod

class Event(metaclass=LittleMeta):
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

    # @abstractmethod
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
            _cache["name"] = line[line.index(" is connecting...")]
            return True
        except ValueError:
            return False

class PlayerConnectEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            _cache["name"] = line[line.index(" connected\x1b[m")]
            return True
        except ValueError:
            return False

class PlayerSpectateEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            _cache["name"] = line[line.index(" is now spectating\x1b[m")]
            return True
        except ValueError:
            return False

class PlayerJoinEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            _cache["name"] = line[line.index(" is now playing\x1b[m")]
            return True
        except ValueError:
            return False

class PlayerDisconnectEvent(Event):
    @classmethod
    def check(cls, line):
        try:
            _cache["name"] = line[line.index(" disconnected\x1b[m")]
            return True
        except ValueError:
            return False


class ChatMsgEvent(Event):
    _chatMsg = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")
    @classmethod
    def check(cls, line):
        temp = cls._chatMsg.match(line)
        if temp:
            _cache["sender"] = temp[0]
            _cache["message"] = temp[1]
            return True
        return False

class FragEvent(Event):
    _fragMsg = re.compile("^(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+.*'s (.*?) \(near (.*)\)(?:,[A-z\s]+(\d+))?|(?:(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? .*?(?:\x1b\[[\d;m]+)+(.*?)(?:\x1b\[[\d;m]+)+).*?(\w+) \(near (.*)\))")
    _cache = {}
    @classmethod
    def check(cls, line):
        temp = cls._fragMsg.match(line)
        if temp:
            temp = tuple(filter(lambda x: x, temp.groups()))
            _cache["victim"] = temp[0]
            _cache["attacker"] = temp[1]
            _cache["weapon"] = temp[2]
            _cache["location"] = temp[3]
            try:
                _cache["fragstreak"] = temp[4]
            except IndexError:
                _cache["fragstreak"] = None
            finally:
                return True
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
    setattr(c, "_handlers", [])
    setattr(c, "_cache", {})
