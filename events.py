
import re

from abc import ABC, abstractmethod

class Event(ABC):
    _handlers = []

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

    @abstractmethod
    def check(*args, **kwargs):
        pass

    def fire(*args, **kwargs):
        for func in Event._handlers:
            func(*args, **kwargs)
    def __new__(cls):
        _events.append(cls)

class PlayerConnectingEvent(Event):
	@classmethod
	def check(cls, line):
		return line.endswith(" is connecting...")


class PlayerConnectEvent(Event):
	@classmethod
	def check(cls, line):
		return line.endswith(" connected\x1b[m")

class PlayerSpectateEvent(Event):
	@classmethod
	def check(cls, line):
		return line.endswith(" is now spectating\x1b[m")

class PlayerJoinEvent(Event):
	@classmethod
	def check(cls, line):
		return line.endswith(" is now playing\x1b[m")

class PlayerDisconnectEvent(Event):
	@classmethod
	def check(cls, line):
		return line.endswith(" disconnected\x1b[m")


class ChatMsgEvent(Event):
    _chatMsg = re.compile("^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)\x1b\[m: (.*)")

    @classmethod
    def check(cls, line):
        return True if _extractMsg.findall(line) else False

class FragEvent(Event):
    _fragMsg = re.compile("^(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*?\x1b\[m(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*?(?:'s (.*?))? \(near (.*)\)")

    @classmethod
    def check(cls, line):
        pass

class SuicideEvent(Event):
    _suicideMsg = re.compile("^(?:\x1b\[\d\;\d+m)?(.*?)\x1b.*? (\w+) \(near (.*?)\)")

    @classmethod
    def check(cls, line):
        pass9

class DebugEvent(Event):
    @classmethod
    def check(cls):
        pass
