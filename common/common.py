from enum import Enum

class requestcode(Enum):
    default = 0
    account = 1
    room = 2

class actioncode(Enum):
    default = 0
    registure = 1
    updateinfo = 2
    clear = 3
    login = 4
    logout = 5
    offline_all = 6

    create = 7
    list = 8
    update = 9
    join = 10
    remove = 11
    clear_empty = 12
    remove_all = 13

class returncode(Enum):
    success = 0
    fail = 1
    cont = 2
    update = 3
    remove = 4