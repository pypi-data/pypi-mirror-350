class CorruptError(Exception):
    """
    The file is corrupt and cannot be opened.


    """
    def __init__(self, message):
        super().__init__(message)
