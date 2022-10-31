"""Tests for the `plu002_visitor` module."""
# pylint: disable=no-self-use,too-few-public-methods
import pytest

from flake8_plus.config import Config
from flake8_plus.visitors.plu002_visitor import PLU002Problem, PLU002Visitor

from .util import generate_bulk_cases, generate_results


class TestPLU002Visitor:
    """Tests for the `PLU002Visitor` class."""

    @pytest.mark.parametrize(
        ("source_code", "expectation", "problems_expected"),
        generate_bulk_cases(PLU002Problem),
    )
    def test_bulk(
        self, source_code: str, expectation: dict[str, int], problems_expected: set[str]
    ):
        """Run bulk test cases."""
        blanks_expected = expectation["blanks_expected"]
        config = Config(blanks_before_return=blanks_expected)
        actual = generate_results(PLU002Visitor, config, source_code)
        assert actual == problems_expected
