"""Problem class."""
# pylint: disable=too-few-public-methods


class Problem:
    """Problem class."""

    code: str

    def __init__(self, line_number: int, col_offset: int, message: str):
        """
        Initialize a `Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            message (str): The message.
        """
        self.line_number = line_number
        self.col_offset = col_offset
        self.message = message

    @property
    def message_with_code(self) -> str:
        """Return the problem message prefixed with with the problem code."""
        code = type(self).code
        return f"{code} {self.message}"
