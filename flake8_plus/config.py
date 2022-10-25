"""Config class."""
# pylint: disable=too-few-public-methods


class Config:
    """Plugin configuration class."""

    def __init__(self, blanks_before_imports: int):
        """
        Initialize a `Configuration` instance.

        Args:
            blanks_before_imports (int): Number of blanks line expected before first
            import statements.
        """
        self.blanks_before_imports = blanks_before_imports
