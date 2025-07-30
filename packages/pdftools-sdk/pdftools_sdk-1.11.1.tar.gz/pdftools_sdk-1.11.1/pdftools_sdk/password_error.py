class PasswordError(Exception):
    """
    Invalid password specified.


    """
    def __init__(self, message):
        super().__init__(message)
