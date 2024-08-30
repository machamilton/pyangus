class AngusRpaException(Exception):
    """
    Exception do Angus Client
    """

    def __init__(self, message):
        super().__init__("Angus RPA Error: " + message)
