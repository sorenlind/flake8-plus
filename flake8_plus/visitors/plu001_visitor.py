"""Exception classes raised by various operations within pylint."""
import ast
from typing import Any

from ..config import Config
from ..problem import Problem


class PLU001Visitor(ast.NodeVisitor):
    """Visitor class for the PLU001 rule."""

    def __init__(self, lines: list[str], config: Config):
        """
        Initialize a PLU001Visitor instance.

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
                problem = Problem(node.lineno, node.col_offset, "PLU001", message)
                self.problems.append(problem)
        elif hasattr(node, "end_lineno") and (node.end_lineno is not None):
            self._last_end = node.end_lineno

    def _compute_blank_before(self, line_number: int) -> int:
        if line_number <= (self._last_end + 1):
            return 0

        indices_reversed = reversed(range(self._last_end, line_number - 1))
        n_blanks = 0
        for index in indices_reversed:
            if self._lines[index].strip():
                break
            n_blanks += 1
        return n_blanks


def _build_message(blanks_actual: int, blanks_expected: int) -> str:
    format_ = "expected {} blank lines before first import, found {}"
    return format_.format(blanks_expected, blanks_actual)
