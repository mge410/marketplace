class CategoryDoesNotExistsException(Exception):
    def __init__(self, message: str = "Category does not exists") -> None:
        self.message = message
