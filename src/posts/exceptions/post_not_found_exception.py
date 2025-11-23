class PostNotFoundException(Exception):
    def __init__(self, message: str = "Post not found") -> None:
        self.message = message
