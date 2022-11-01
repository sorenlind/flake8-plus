"""Base class for visitors used in Flake8-plus."""
import ast
from typing import Any

from ..config import Config
from ..exceptions import MultipleStatementsError
from ..problem import Problem


class BaseVisitor(ast.NodeVisitor):
    """Base class for visitors used in Flake8-plus."""

    def __init__(self, lines: list[str], config: Config):
        """
        Initialize BaseVisitor instance.

        Args:
            lines (list[str]): The physical lines.
            config (Config): Configuration instance for the plugin and visitor.
        """
        self.problems: list[Problem] = []
        self._lines = lines
        self.config = config
        self._previous_node = None

    def visit(self, node: ast.AST) -> Any:
        """
        Visit an `AST` instance.

        Args:
            node (ast.AST): The abstract syntax tree to visit.

        Returns:
            Any: The result of calling `visit` on the super class.
        """
        result = super().visit(node)
        self._previous_node = node
        return result

    def compute_blanks_before(self, node: ast.AST) -> int:
        """
        Compute the number of blank immediately preceding the specified line number.

        Args:
            line_number (int): The line number to check for blank lines before.

        Returns:
            int: The number of blank lines.
        """
        line_index = node.lineno - 1
        line = self._lines[line_index]
        line_offset = len(line) - len(line.lstrip())
        if line_offset != node.col_offset:
            raise MultipleStatementsError(f"Multiple statements on line {node.lineno}")

        indices_reversed = reversed(range(0, line_index))
        n_blanks = 0
        for index in indices_reversed:
            if self._lines[index].strip():
                break
            n_blanks += 1
        return n_blanks
