"""Config class."""
# pylint: disable=too-few-public-methods
from . import defaults


class Config:
    """Plugin configuration class."""

    def __init__(
        self,
        blanks_before_imports: int = defaults.BLANKS_BEFORE_IMPORTS,
        blanks_before_return: int = defaults.BLANKS_BEFORE_RETURN,
        blanks_before_except: int = defaults.BLANKS_BEFORE_EXCEPT,
    ):
        """
        Initialize a `Configuration` instance.

        Args:
            blanks_before_imports (int): Number of blanks line expected before first
                import statements.
            blanks_before_return (int): Number of blanks line expected before return
                statement.
            blanks_before_except (int): Number of blanks line expected before except.
        """
        self.blanks_before_imports = blanks_before_imports
        self.blanks_before_return = blanks_before_return
        self.blanks_before_except = blanks_before_except
