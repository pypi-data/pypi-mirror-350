from enum import Enum


class DatabaseStatus(Enum):
    UNKNOWN = 0
    NOT_CREATED = 1
    NOT_RUNNING = 2
    RUNNING = 3
