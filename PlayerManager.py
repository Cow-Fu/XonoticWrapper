import events
from enum import Enum
import re
from collections import namedtuple
from LineParser import stripSpecialChars
from events import PlayerJoinEvent, PlayerConnectEvent, PlayerSpectateEvent, PlayerConnectingEvent, PlayerDisconnectEvent


class PLAYERSTATUS(Enum):
    CONNECTED = 1
    SPECTATING = 2
    PLAYING = 3
    DISCONNECTED = 4

_playerFactory = namedtuple("Player", ["name", "status", "score"])
Player = lambda name, status, score=-666: _playerFactory(name, status, score)

# _extractName = re.compile(r"^(?:\x1b\[m|\x1b\[\d\;\d+m)*(.*?)(?:\x1b)")

_players = []

def _changePlayerStatus(playerName, status):
    print(_players)
    # temp = _extractName.match(playerName)
    if temp:
        name = temp.groups()[0]
        for player in _players:
            print("{}=={}=={}".format(player.name, name, player.name == name))
            if player.name == name:
                player.status = status
                return
        _players.append(Player(playerName, status))

def stripName(line):
    temp = PlayerManager._extractName(line)
    if temp:
        return temp.groups()[0]
    return None

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
