class HttpError(Exception):
    """
    An error occurred during the processing of a HTTP request.


    """
    def __init__(self, message):
        super().__init__(message)
