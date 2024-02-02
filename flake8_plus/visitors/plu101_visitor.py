"""Problem 101: Python code in comment."""
# pylint: disable=too-few-public-methods
import ast
from typing import Any

from ..problem import Problem
from .base_visitor import BaseVisitor


class PLU101Problem(Problem):
    """Problem 101: Python code in comment."""

    code = "PLU101"

    def __init__(  # pylint: disable=unused-argument
        self,
        line_number: int,
        col_offset: int,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize a `PLU101Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            blanks_actual (int): Number of actual blanks before except.
            blanks_expected (int): Number of expected blanks before except.
        """
        message = "Python code in comment."
        super().__init__(line_number, col_offset, message)


class PLU101Visitor(ast.NodeVisitor):
    """Visitor class for the PLU101 rule."""

    def vist_Comment():
        # Ouch, ASTs can't do that!
