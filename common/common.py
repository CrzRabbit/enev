from enum import Enum

class requestcode(Enum):
    default = 0
    account = 1
    room = 2

class actioncode(Enum):
    default = 0
    registure = 1
    updatepwd = 2
    clear = 3
    login = 4
    logout = 5

    create = 6
    list = 7
    update = 8
    join = 9
    remove = 10

class returncode(Enum):
    success = 0
    fail = 1