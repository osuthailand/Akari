from enum import IntFlag

class Privileges(IntFlag):
    ACCESS = 1 << 3

    # Manage privileges; The most important privileges
    MANAGE_USERS = 1 << 4
    MANAGE_BEATMAPS = 1 << 8
    MANAGE_SERVERS = 1 << 9
    MANAGE_SETTINGS = 1 << 10
    # MANAGE_KEYS = 1 << 11; Not used.
    MANAGE_REPORTS = 1 << 12
    # MANAGE_DOCS = 1 << 13; Not used.
    MANAGE_BADGES = 1 << 14
    MANAGE_PRIV = 1 << 16

    # I don't know lol.
    VIEW_LOGS = 1 << 15
    SEND_ALERTS = 1 << 17
    CHAT_MOD = 1 << 18

    # Big boy perms.
    BAN_USERS = 1 << 5
    SILENCE_USERS = 1 << 6
    WIPE_USERS = 1 << 7
    KICK_USERS = 1 << 19
    
    