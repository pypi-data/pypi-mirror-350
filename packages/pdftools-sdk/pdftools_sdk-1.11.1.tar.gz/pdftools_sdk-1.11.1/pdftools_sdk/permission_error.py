class PermissionError(Exception):
    """
    The operation is not allowed.


    """
    def __init__(self, message):
        super().__init__(message)
