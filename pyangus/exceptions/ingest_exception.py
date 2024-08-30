class AngusIngestException(Exception):
    """
    Exception Angus Ingest
    """

    def __init__(self, message):
        super().__init__("Angus Ingest Error: " + message)
