from blinker import signal
# from enum import Enum

class Events:
    PLAYER_CONNECTED = signal("playerConnected")
    PLAYER_DISCONNECT = signal("playerDisconnect")
    PLAYER_CONNECTING = signal("playerConnecting")
    PLAYER_SPECTATE = signal("playerSpectate")
    PLAYER_JOIN = signal("playerJoin")
    CHATMSG = signal("chatMsg")
    DEBUG = signal("debug")
# TODO: add team join event
# TODO: add quad event
# TODO: add flag capture event
# TODO: add flag score event
