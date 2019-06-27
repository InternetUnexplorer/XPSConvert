from typing import Optional


class ParseError(BaseException):
    def __init__(self, message: str, filename: str, line: Optional[int] = None) -> None:
        location = f"{filename}:{line + 1}" if line is not None else filename
        super().__init__(f"{location}: {message}")
