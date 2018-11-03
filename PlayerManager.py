import events
from enum import Enum
import re


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4


class Player:
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        self._status = status

    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, score):
        self._score = score

    def addToScore(self, x=1):
        self._score += x

    def __init__(self, name, status, score=-666):
        self._name = name
        self._status = status
        self._score = score


def _changePlayerStatus(playerName, status):
    temp = _extractName.match(playerName)
    if temp:
        name = temp.groups()[0]
        for player in _players:
            if player.name == name:
                player.status = status
                break

@events.PlayerConnectEvent.connect
def _playerStatusOnConnect(playerName):
    # Events.PLAYER_JOIN.
    _changePlayerStatus(playerName, PLAYERSTATUS.CONNECTED)

@events.PlayerSpectateEvent.connect
def _playerStatusOnSpectate(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.SPECTATING)

@events.PlayerSpectateEvent.connect
def _playerStatusOnJoin(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.PLAYING)

@events.PlayerDisconnectEvent.connect
def _playerStatusOnDisconnect(playerName):
    _changePlayerStatus(playerName, PLAYERSTATUS.DISCONNECTED)

def _getPlayersByStatus(status):
    return list(filter(lambda p: p.status == status, _players))

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

# def _cleanup():
#     global _players
#     temp = {}
#     for k, v in _players.items():
#         if k.startswith(_prefix):
#             temp[k] = v
#     _players = temp

_prefix = "\x1b[1;33m\x1b[m"
_extractName = re.compile(r"^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)(?:\x1b)")
_players = []
