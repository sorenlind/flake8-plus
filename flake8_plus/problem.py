"""Problem class."""
# pylint: disable=too-few-public-methods


class Problem:
    """Problem class."""

    message_format: str

    def __init__(self, line_number: int, col_offset: int, code: str, message: str):
        """
        Initialize a `Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            code (str): The problem code.
            message (str): The message.
        """
        self.line_number = line_number
        self.col_offset = col_offset
        self.formatted_message = f"{code} {message}"
