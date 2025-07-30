class ProcessingError(Exception):
    """
    The file cannot be processed.


    """
    def __init__(self, message):
        super().__init__(message)
