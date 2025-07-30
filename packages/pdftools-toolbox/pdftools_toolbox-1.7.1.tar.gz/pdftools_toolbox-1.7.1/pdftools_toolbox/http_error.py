class HttpError(Exception):
    """
    An error occurred while processing an HTTP request.


    """
    def __init__(self, message):
        super().__init__(message)
