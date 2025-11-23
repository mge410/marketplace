class IncorrectPasswordException(Exception):
    def __init__(self, message: str = "Incorrect password") -> None:
        self.message = message
