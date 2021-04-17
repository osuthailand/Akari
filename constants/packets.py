from enum import IntEnum, unique

@unique
class Packets(IntEnum):
    AKARI_END_EVENT = 200
    AKARI_START_EVENT = 201