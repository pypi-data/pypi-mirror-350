class ConformanceError(Exception):
    """
    The document has an invalid conformance level.


    """
    def __init__(self, message):
        super().__init__(message)
