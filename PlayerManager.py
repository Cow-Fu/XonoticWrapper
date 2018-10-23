from events import Events
from enum import Enum
import re


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4


class Player:
    def getName(self, name):
        return self.name

    def getScore(self, score):
        return self.score

    def getStatus(self, status):
        return self.status

    def changeName(self, name):
        self.name = name

    def addToScore(self, x=1):
        self.score += x

    def setStatus(self, status):
        self.status = status

    def __init__(self, name, status, score=-666):
        self.name = name
        self.status = status
        self.score = score


def _changePlayerStatus(playerName, status):
    temp = _extractName.match(playerName)
    if temp:
        name = temp.groups()[0]
        for player in _players:
            if player.getName() == name:
                player.setStatus(status)
                break

@Events.PLAYER_CONNECTED.connect
def _playerStatusOnConnect(playerName):
    # Events.PLAYER_JOIN.
    _changePlayerStatus(playerName, PLAYERSTATUS.CONNECTED)

@Events.PLAYER_SPECTATE.connect
def _playerStatusOnSpectate(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.SPECTATING)

@Events.PLAYER_JOIN.connect
def _playerStatusOnJoin(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.PLAYING)

@Events.PLAYER_DISCONNECT.connect
def _playerStatusOnDisconnect(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.DISCONNECTED)

def _getPlayersByStatus(status):
    return list(filter(lambda p: p.getStatus() == status, _players))

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
_extractName = re.compile(r"^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)(?:\x1b)")
# _suffix =
_players = []
