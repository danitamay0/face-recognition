# face/exceptions.py
class InvalidFileExtensionError(Exception):
    def __init__(self, message="Invalid file extension"):
        self.message = message
        super().__init__(self.message)