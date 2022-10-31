"""Exception classes raised by various operations within pylint."""
# pylint: disable=too-few-public-methods
import ast
from typing import Any

from ..config import Config
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

    def __init__(self, lines: list[str], config: Config):
        """
        Initialize a PLU002Visitor instance.

        Args:
            lines (list[str]): The physical lines.
            config (Config): Configuration instance for the plugin and visitor.
        """
        self._last_end: int = 0
        super().__init__(lines, config)

    def visit(self, node: ast.AST) -> Any:
        """
        Visit the specified node.

        Args:
            node (ast.AST): The node to visit.

        Returns:
            Any: The value returned by the base class `visit` method.
        """
        self._process_node(node)
        return super().visit(node)

    def _process_node(self, node: ast.AST):
        if isinstance(node, ast.Return):
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
        elif hasattr(node, "end_lineno") and (node.end_lineno is not None):
            self._last_end = node.end_lineno
