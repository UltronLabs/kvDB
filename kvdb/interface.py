import os
from .storage import Storage
from .binary_tree import BinaryTree


class KVDB(object):
    """
    A key value database class that uses a binary tree for storing data.
    It provides methods for getting and setting values for keys.
    """

    # Initializing the KVDB object with a file for storage and a binary tree for data organization
    def __init__(self, f):
        super().__init__()
        self._storage = Storage(f)  # Creating a Storage object with the provided file
        self._tree = BinaryTree(
            self._storage
        )  # Creating a BinaryTree object with the created Storage object

    def __getitem__(self, key):
        self.__assert_not_closed()
        return self._tree.get(key)

    def __setitem__(self, key, value):
        self._assert_not_closed()
        return self._tree.set(key, value)

    def _assert_not_closed(self):
        #  # Ensuring that the database is still open before interacting with db layer
        if self._storage.closed:
            raise ValueError("Database Closed.")

    def commit(self):
        self._assert_not_closed()
        self._tree.commit()

    def connect(dbname):
        try:
            f = open(dbname, "r+b")
        except IOError:
            fd = os.open(dbname, os.O_RDWR | os.O_CREAT)
            f = os.fdopen(fd, "w+b")  # Change this line

        return KVDB(f)

    def some_method(self):
        self.__assert_not_closed()

    def __assert_not_closed(self):
        pass
