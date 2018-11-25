import events
from enum import Enum
import re
from LineParser import stripSpecialChars, _REPLACE_CHAR
from events import PlayerJoinEvent, PlayerConnectEvent, PlayerSpectateEvent, PlayerConnectingEvent, PlayerDisconnectEvent


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4

class Player:
    def __init__(self, name, parsedName, status, score=-666):
        self.name = name
        self.parsedName = parsedName
        self.status = status
        self.score = score

_players = []

def _changePlayerStatus(playerName, status):
    parsedName = "".join(stripSpecialChars(playerName)).replace(_REPLACE_CHAR, "")

    for player in _players:
        if player.parsedName == parsedName:
            player.status = status
            return
    _players.append(Player(playerName, parsedName, status))


@PlayerConnectEvent.connect
def _playerStatusOnConnect(name):
    # Events.PLAYER_JOIN.
    _changePlayerStatus(name, PLAYERSTATUS.CONNECTED)

@events.PlayerSpectateEvent.connect
def _playerStatusOnSpectate(name):
    _changePlayerStatus(name, PLAYERSTATUS.SPECTATING)

@events.PlayerSpectateEvent.connect
def _playerStatusOnJoin(name):
    _changePlayerStatus(name, PLAYERSTATUS.PLAYING)

@events.PlayerDisconnectEvent.connect
def _playerStatusOnDisconnect(name):
    _changePlayerStatus(name, PLAYERSTATUS.DISCONNECTED)

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
