import events
from enum import Enum
import re
from collections import namedtuple
from events import PlayerJoinEvent, PlayerConnectEvent, PlayerSpectateEvent, PlayerConnectingEvent, PlayerDisconnectEvent


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4

_player = namedtuple("Player", ["name", "status", "score"])
Player = lambda name, status, score=-666: _player(name, status, score)

class PlayerManager:
    _extractName = re.compile(r"^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)(?:\x1b)")

    def __init__(self):
        self._players = []

    def _changePlayerStatus(self, playerName, status):
        temp = PlayerManager._extractName.match(playerName)
        if temp:
            name = temp.groups()[0]
            for player in self._players:
                if player.name == name:
                    player.status = status
                    break

    @staticmethod
    def stripName(line):
        temp = PlayerManager._extractName(line)
        if temp:
            return temp.groups()[0]
        return None

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
        return self._players

    def getConnectedPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.CONNECTED)

    def getSpectatingPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.SPECTATING)

    def getPlayingPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.PLAYING)

    def getDisconnectedPlayers(self):
        return self._getPlayersByStatus(PLAYERSTATUS.DISCONNECTED)
