"""Exception classes raised by various operations within pylint."""
# pylint: disable=too-few-public-methods
import ast
from typing import Any

from ..config import Config
from ..problem import Problem
from .base_visitor import BaseVisitor


class PLU001Problem(Problem):
    """Problem 001: Number of blank lines before first import."""

    code = "PLU001"
    format_ = "expected {} blank lines before first import, found {}"

    def __init__(  # pylint: disable=unused-argument
        self,
        line_number: int,
        col_offset: int,
        blanks_actual: int,
        blanks_expected: int,
        **kwargs: dict[str, Any],
    ):
        """
        Initialize a `PLU001Problem` instance.

        Args:
            line_number (int): The line number.
            col_offset (int): The column offset.
            blanks_actual (int): Number of actual blanks before first import.
            blanks_expected (int): Number of expected blanks before first import.
        """
        message = PLU001Problem.format_.format(blanks_expected, blanks_actual)
        super().__init__(line_number, col_offset, message)


class PLU001Visitor(BaseVisitor):
    """Visitor class for the PLU001 rule."""

    def __init__(self, lines: list[str], config: Config):
        """
        Initialize a PLU001Visitor instance.

        Args:
            lines (list[str]): The physical lines.
            config (Config): Configuration instance for the plugin and visitor.
        """
        self._previous_import = False
        super().__init__(lines, config)

    def visit_Import(self, node: ast.Import) -> Any:
        """
        Visit an `Import` node.

        Args:
            node (ast.Import): The node to visit.

        Returns:
            Any: The result of calling `generic_visit`.
        """
        # pylint: disable=invalid-name
        self._process_import(node)
        return self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """
        Visit an `ImportFrom` node.

        Args:
            node (ast.Import): The node to visit.

        Returns:
            Any: The result of calling `generic_visit`.
        """
        # pylint: disable=invalid-name
        self._process_import(node)
        return self.generic_visit(node)

    def _process_import(self, node: ast.AST):
        if self._previous_import:
            return

        self._previous_import = True
        if node.col_offset != 0:
            # Either a non-top-level import, or there are multiple
            # statements on one line.
            return

        actual = self.compute_blanks_before(node)

        if actual != self.config.blanks_before_imports:
            problem = PLU001Problem(
                node.lineno,
                node.col_offset,
                actual,
                self.config.blanks_before_imports,
            )
            self.problems.append(problem)
