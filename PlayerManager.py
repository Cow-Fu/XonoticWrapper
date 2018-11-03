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

class PlayerManager:
    _extractName = re.compile(r"^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)(?:\x1b)")

    def _changePlayerStatus(self, playerName, status):
        temp = PlayerManager._extractName.match(playerName)
        if temp:
            name = temp.groups()[0]
            for player in self._players:
                if player.name == name:
                    player.status = status
                    break

    @events.PlayerConnectEvent.connect
    def _playerStatusOnConnect(self, playerName):
        # Events.PLAYER_JOIN.
        self._changePlayerStatus(playerName, PLAYERSTATUS.CONNECTED)

    @events.PlayerSpectateEvent.connect
    def _playerStatusOnSpectate(self, playerName):
        self._changePlayerStatus(playerName, PLAYERSTATUS.SPECTATING)

    @events.PlayerSpectateEvent.connect
    def _playerStatusOnJoin(self, playerName):
        self._changePlayerStatus(playerName, PLAYERSTATUS.PLAYING)

    @events.PlayerDisconnectEvent.connect
    def _playerStatusOnDisconnect(self, playerName):
        self._changePlayerStatus(playerName, PLAYERSTATUS.DISCONNECTED)

    def _getPlayersByStatus(self, status):
        return list(filter(lambda p: p.status == status, self._players))

    def getPlayers(self):
        return self_players

    def getConnectedPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.CONNECTED)

    def getSpectatingPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.SPECTATING)

    def getPlayingPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.PLAYING)

    def getDisconnectedPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.DISCONNECTED)

    def __init__(self):
        self._players = []
