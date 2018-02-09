from enum import Enum

class requestcode(Enum):
    default = 0
    account = 1
    logio = 2

class actioncode(Enum):
    default = 0
    registure = 1
    updatepwd = 2
    login = 3
    logout = 4

