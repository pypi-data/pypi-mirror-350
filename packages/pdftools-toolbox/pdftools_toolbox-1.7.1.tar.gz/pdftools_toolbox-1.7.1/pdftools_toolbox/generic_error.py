class GenericError(Exception):
    """
    A generic error occurred.


    """
    def __init__(self, message):
        super().__init__(message)
