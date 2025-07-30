class ExistsError(Exception):
    """
    The specified item already exists.


    """
    def __init__(self, message):
        super().__init__(message)
