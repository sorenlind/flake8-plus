"""Exception classes raised by various operations within pylint."""
# pylint: disable=too-few-public-methods
import ast
from typing import Any

from ..exceptions import MultipleStatementsError
from ..problem import Problem
from .base_visitor import BaseVisitor


class PLU002Problem(Problem):
    """Problem 002: Number of blank lines before return statement."""

    code = "PLU002"
    format_ = "expected {} blank lines before return statement, found {}"

    def __init__(  # pylint: disable=unused-argument
        self,
        line_number: int,
        col_offset: int,
        blanks_actual: int,
        blanks_expected: int,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize a `PLU002Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            blanks_actual (int): Number of actual blanks before return statement.
            blanks_expected (int): Number of expected blanks before return statement.
        """
        message = PLU002Problem.format_.format(blanks_expected, blanks_actual)
        super().__init__(line_number, col_offset, message)


class PLU002Visitor(BaseVisitor):
    """Visitor class for the PLU002 rule."""

    def visit_Return(self, node: ast.Return) -> Any:
        """
        Visit a `Return` node.

        Args:
            node (ast.Return): The node to visit.

        Returns:
            Any: The result of calling `generic_visit`.
        """
        # pylint: disable=invalid-name
        if not isinstance(self._previous_node, ast.FunctionDef | ast.ClassDef):
            self._process_node(node)
        return self.generic_visit(node)

    def _process_node(self, node: ast.Return):
        try:
            actual = self.compute_blanks_before(node)
        except MultipleStatementsError:
            return

        if actual != self.config.blanks_before_return:
            problem = PLU002Problem(
                node.lineno,
                node.col_offset,
                actual,
                self.config.blanks_before_return,
            )
            self.problems.append(problem)
