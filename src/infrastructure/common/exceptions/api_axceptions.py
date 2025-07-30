from typing import Any


class RouterInitializationError(Exception):
    _message = "Error while router serialization"

    def __init__(self, data: Any | None) -> None:
        self.data = data
        super().__init__(self._message)

    def __str__(self) -> str:
        return (
            f"Initialization Error: {self._message} - Data: {self.data}"
            if self.data
            else f"Initialization Error: {self._message}"
        )
