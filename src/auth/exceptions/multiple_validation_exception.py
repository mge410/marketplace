from typing import List, Any
from dataclasses import dataclass


@dataclass
class ValidationError:
    field: str
    message: str
    value: Any


class MultipleValidationException(Exception):
    def __init__(self, errors: List[ValidationError]):
        self.errors = errors
        super().__init__(f"Validation failed with {len(errors)} errors")

    def to_response(self) -> list[dict[str, Any]]:
        return [
            {"field": error.field, "message": error.message, "value": error.value}
            for error in self.errors
        ]
