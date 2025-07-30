class RetryError(Exception):
    """
    A resource or service is temporarily unavailable.


    """
    def __init__(self, message):
        super().__init__(message)
