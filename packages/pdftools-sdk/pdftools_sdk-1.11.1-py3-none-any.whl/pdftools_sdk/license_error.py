class LicenseError(Exception):
    """
    The license is not valid.


    """
    def __init__(self, message):
        super().__init__(message)
