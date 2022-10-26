"""Tests for the plugin module."""
# pylint: disable=no-self-use,protected-access
import ast

from flake8_plus import Plugin
from flake8_plus.config import Config


def _results(code: str, blanks_before_imports: int) -> set[str]:
    tree = ast.parse(code)
    Plugin.config = Config(blanks_before_imports)
    plugin = Plugin(tree, code.split("\n"))
    return {f"{line}:{col+1} {msg}" for line, col, msg, _ in plugin.run()}


class TestPlugin:
    """Tests for the Plugin class."""

    def test_plu001_empty_code(self):
        """Test that empty code results in no errors."""
        assert _results("", 0) == set()

    def test_plu001_docstring_excessive_whitespace(self):
        """Test that a problem is detected for docstring, blank line, import."""
        expected = {"3:1 PLU001 expected 0 blank lines before first import, found 1"}
        code = '"""Docstring."""\n\nimport ast\n'
        actual = _results(code, 0)
        assert actual == expected

    def test_plu001_docstring_pylint_ok(self):
        """Test that a problem is detected for docstring, comment, import."""
        expected = set()
        code = '"""Docstring."""\n# pylint: disable=no-self-use\nimport ast\n'
        actual = _results(code, 0)
        assert actual == expected

    def test_plu001_simple_no_whitespace_ok(self):
        """Test that no problem is detected for docstring, comment, import."""
        code = '"""Docstring."""\nimport ast'
        assert _results(code, 0) == set()
