"""The flake8-plus visitor."""
import ast
from typing import Any

from ..config import Config
from ..problem import Problem


class PLU100Visitor(ast.NodeVisitor):
    """Visitor class for the PLU100 rule."""

    def __init__(self, lines: list[str], config: Config):
        """
        Initialize a PLU100Visitor instance.

        Args:
            lines (list[str]): The physical lines.
            config (Config): Configuration instance for the plugin and visitor.
        """
        self._last_end: int = 0
        self._previous_import = False
        self.problems: list[Problem] = []
        self._lines = lines
        self.config = config

    def visit(self, node: ast.AST) -> Any:
        """
        Visit the specified node.

        Args:
            node (ast.AST): The node to visit.

        Returns:
            Any: The value returned by the base class `visit` method.
        """
        if not self._previous_import:
            self._process_node(node)
        return super().visit(node)

    def _process_node(self, node: ast.AST):
        if isinstance(node, ast.Import | ast.ImportFrom):
            self._previous_import = True
            actual = self._compute_blank_before(node.lineno)
            if actual != self.config.blanks_before_imports:
                message = _build_message(actual, self.config.blanks_before_imports)
                problem = Problem(node.lineno, node.col_offset, "PLU100", message)
                self.problems.append(problem)
        elif hasattr(node, "end_lineno") and (node.end_lineno is not None):
            self._last_end = node.end_lineno

    def _compute_blank_before(self, line_number: int) -> int:
        if line_number <= (self._last_end + 1):
            return 0

        line_numbers = range(self._last_end + 1, line_number)
        blanks = [l for l in line_numbers if not self._lines[l - 1].strip()]
        return len(blanks)


def _build_message(blanks_actual: int, blanks_expected: int) -> str:
    format_ = "expected {} blank lines before first import, found {}"
    return format_.format(blanks_expected, blanks_actual)
