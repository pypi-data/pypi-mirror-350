class UnsupportedFeatureError(Exception):
    """
    The document contains an unsupported feature.


    """
    def __init__(self, message):
        super().__init__(message)
