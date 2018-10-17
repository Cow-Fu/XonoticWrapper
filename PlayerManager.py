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

def _getPlayersByStatus(status):
    temp = {}
    for k, v in _players.items():
        if x == status:
            temp[k] = v
    return temp

def getPlayers():
    return _players

def getConnectedPlayers():
    return _getPlayersByStatus(PLAYERSTATUS.CONNECTED)

def getSpectatingPlayers():
    return _getPlayersByStatus(PLAYERSTATUS.SPECTATING)

def getPlayingPlayers():
    return _getPlayersByStatus(PLAYERSTATUS.PLAYING)

def getDisconnectedPlayers():
    return _getPlayersByStatus(PLAYERSTATUS.DISCONNECTED)

def _cleanup():
    global _players
    temp = {}
    for k, v in _players.items():
        if k.startswith(_prefix):
            temp[k] = v
    _players = temp

_prefix = "\x1b[1;33m\x1b[m"
# _suffix =
_players = {}
