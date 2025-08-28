class CategoryAlreadyExistsException(Exception):
    def __init__(self, message: str = "Category already exists") -> None:
        self.message = message
