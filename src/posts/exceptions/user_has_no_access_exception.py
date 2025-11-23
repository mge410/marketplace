class UserHasNoAccessException(Exception):
    def __init__(self, message: str = "Only author can update the post") -> None:
        self.message = message
