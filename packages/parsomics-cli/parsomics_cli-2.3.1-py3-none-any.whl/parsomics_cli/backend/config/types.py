from enum import Enum


class Scope(str, Enum):
    USER = "user"
    SYSTEM = "system"
    CUSTOM = "custom"
