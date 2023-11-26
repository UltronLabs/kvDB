import portalocker


class Storage:
    # ...
    def __init__(self, file) -> None:
        self.file = file
        self.locked = False
        self.get_root_address = None

    def lock(self):
        """
        This method is used to lock the file for exclusive access.

        If the file is not already locked (i.e., self.locked is False), it uses the portalocker library
        to lock the file. The portalocker.LOCK_EX argument indicates that it's an exclusive lock,
        meaning no other process can access the file while it's locked.

        After successfully locking the file, it sets self.locked to True and returns True to indicate
        that the file was successfully locked.

        If the file is already locked (i.e., self.locked is True), it simply returns False.
        """
        if not self.locked:
            portalocker.lock(self._f, portalocker.LOCK_EX)
            self.locked = True
            return True
        else:
            return False

    def commit_root_address(self, root_address):
        """
        This method locks the file, flushes any buffered data,
        seeks to the superblock, writes the root address,
        flushes again and then unlocks the file.
        """

        # Lock the file to prevent other processes from accessing it simultaneously.
        self.lock()

        # Flush the buffer, writing any buffered data to disk.
        self._f.flush()

        # Seek to the position of the superblock in the file.
        self._seek_superblock()

        # Write the root address to the superblock.
        self._write_integer(root_address)

        # Flush the buffer again to ensure that the root address is written to disk.
        self._f.flush()

        # Unlock the file, allowing other processes to access it.
        self.unlock()
