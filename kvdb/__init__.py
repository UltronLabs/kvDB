import os
from kvdb.interface import KVDB


def connect(dbname):
    try:
        f = open(dbname, "r+b")
    except IOError:
        fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
        f = os.fdopen(fd, "w+b")  # Change this line

    return KVDB(f)
