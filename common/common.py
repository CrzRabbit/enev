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
    offline_all = 12

    create = 6
    list = 7
    update = 8
    join = 9
    remove = 10
    clear_empty = 11
    remove_all = 13

class returncode(Enum):
    success = 0
    fail = 1
    cont = 2