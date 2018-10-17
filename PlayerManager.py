from events import Events
from enum import Enum


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4

def changePlayerStatus(playerName, status):
    _players[playerName] = status
    _cleanup()

@Events.PLAYERCONNECTED.connect
def playerStatusOnConnect(playerName):
    changePlayerStatus(playerName, PLAYERSTATUS.CONNECTED)

@Events.PLAYERSPECTATE.connect
def playerStatusOnSpectate(playerName):
    changePlayerStatus(playerName, PLAYERSTATUS.SPECTATING)

@Events.PLAYERJOIN.connect
def playerStatusOnJoin(playerName):
    changePlayerStatus(playerName, PLAYERSTATUS.PLAYING)

@Events.PLAYERDISCONNECT.connect
def playerStatusOnDisconnect(playerName):
    changePlayerStatus(playerName, PLAYERSTATUS.DISCONNECTED)

def getPlayers():
    return _players

def getConnectedPlayers():
    temp = {}
    for k, v in _players.items():
        if x == PLAYERSTATUS.CONNECTED:
            temp[k] = v
    return temp

def getSpectatingPlayers():
    temp = {}
    for k, v in _players.items():
        if x == PLAYERSTATUS.SPECTATING:
            temp[k] = v
    return temp

def getPlayingPlayers():
    temp = {}
    for k, v in _players.items():
        if x == PLAYERSTATUS.PLAYING:
            temp[k] = v
    return temp

def getDisconnectedPlayers():
    temp = {}
    for k, v in _players.items():
        if x == PLAYERSTATUS.DISCONNECTED:
            temp[k] = v
    return temp

def _cleanup():
    global _players
    temp = {}
    for k, v in _players.items():
        if k.startswith(_prefix):
            temp[k] = v
    _players = temp

_prefix = "\x1b[1;33m\x1b[m"
_players = {}
