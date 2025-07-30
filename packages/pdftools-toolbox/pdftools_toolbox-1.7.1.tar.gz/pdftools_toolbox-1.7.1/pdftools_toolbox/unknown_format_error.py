class UnknownFormatError(Exception):
    """
    The format is not known.


    """
    def __init__(self, message):
        super().__init__(message)
