"""The flake8-plus plugin."""
# pylint: disable=too-few-public-methods
import ast
from argparse import Namespace
from typing import Any, Generator, Type

from flake8.options.manager import OptionManager

from . import defaults
from .config import Config
from .version import VERSION
from .visitors.plu001_visitor import PLU001Visitor
from .visitors.plu002_visitor import PLU002Visitor
from .visitors.plu003_visitor import PLU003Visitor


class Plugin:
    """Flake8-plus plugin."""

    name = "flake8-plus"
    version = VERSION
    visitors = [
        PLU001Visitor,
        PLU002Visitor,
        PLU003Visitor,
    ]

    def __init__(self, tree: ast.AST, lines: list[str]):
        """
        Initialize a Plugin instance.

        Args:
            tree (ast.AST): The abstract syntax tree.
            lines (list[str]): The physical lines.
        """
        self._tree = tree
        self._lines = lines

    def run(self) -> Generator[tuple[int, int, str, Type[Any]], None, None]:
        """
        Run the plugin.

        Yields:
            Generator[tuple[int, int, str, Type[Any]], None, None]: Generator of
            problems found.
        """
        for cls in Plugin.visitors:
            visitor = cls(self._lines, Plugin.config)
            visitor.visit(self._tree)
            for p in visitor.problems:
                yield p.line_number, p.col_offset, p.message_with_code, type(self)

    @staticmethod
    def add_options(option_manager: OptionManager) -> None:  # pragma: no cover
        """Add custom configuration option(s) to flake8."""
        option_manager.add_option(
            "--blanks-before-imports",
            type="int",
            metavar="n",
            default=defaults.BLANKS_BEFORE_IMPORTS,
            parse_from_config=True,
            help="Expected number of blank lines before toplevel imports. "
            "(Default: %(default)s)",
        )

        option_manager.add_option(
            "--blanks-before-return",
            type="int",
            metavar="n",
            default=defaults.BLANKS_BEFORE_RETURN,
            parse_from_config=True,
            help="Expected number of blank lines before return statement. "
            "(Default: %(default)s)",
        )

        option_manager.add_option(
            "--blanks-before-except",
            type="int",
            metavar="n",
            default=defaults.BLANKS_BEFORE_EXCEPT,
            parse_from_config=True,
            help="Expected number of blank lines before except. (Default: %(default)s)",
        )

    @classmethod
    def parse_options(cls, options: Namespace) -> None:  # pragma: no cover
        """Parse the custom configuration options given to flake8."""
        cls.config = Config(
            options.blanks_before_imports,
            options.blanks_before_return,
            options.blanks_before_except,
        )
