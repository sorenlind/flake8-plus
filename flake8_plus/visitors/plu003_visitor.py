"""Exception classes raised by various operations within pylint."""
# pylint: disable=too-few-public-methods
import ast
from typing import Any

from ..problem import Problem
from .base_visitor import BaseVisitor


class PLU003Problem(Problem):
    """Problem 003: Number of blank lines before except."""

    code = "PLU003"
    format_ = "expected {} blank lines before except, found {}"

    def __init__(  # pylint: disable=unused-argument
        self,
        line_number: int,
        col_offset: int,
        blanks_actual: int,
        blanks_expected: int,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize a `PLU003Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            blanks_actual (int): Number of actual blanks before except.
            blanks_expected (int): Number of expected blanks before except.
        """
        message = PLU003Problem.format_.format(blanks_expected, blanks_actual)
        super().__init__(line_number, col_offset, message)


class PLU003Visitor(BaseVisitor):
    """Visitor class for the PLU003 rule."""

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> Any:
        """
        Visit a `ExceptHandler` node.

        Args:
            node (ast.ExceptHandler): The node to visit.

        Returns:
            Any: The result of calling `generic_visit`.
        """
        # pylint: disable=invalid-name
        actual = self.compute_blanks_before(node)
        if actual != self.config.blanks_before_except:
            problem = PLU003Problem(
                node.lineno,
                node.col_offset,
                actual,
                self.config.blanks_before_except,
            )
            self.problems.append(problem)
        return self.generic_visit(node)
