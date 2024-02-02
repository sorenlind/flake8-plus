"""Tests for the `plu101_visitor` module."""
# pylint: disable=no-self-use,too-few-public-methods
import pytest

from flake8_plus.config import Config
from flake8_plus.visitors.plu101_visitor import PLU101Problem, PLU101Visitor

from .util import generate_bulk_cases, generate_results


class TestPLU101Visitor:
    """Tests for the `PLU101Visitor` class."""

    @pytest.mark.parametrize(
        ("source_code", "expectation", "problems_expected"),
        generate_bulk_cases(PLU101Problem),
    )
    def test_bulk(  # pylint: disable=unused-argument
        self,
        source_code: str,
        expectation: dict[str, int],
        problems_expected: set[tuple[int, int, str]],
    ):
        """Run bulk test cases."""
        config = Config()
        actual = generate_results(PLU101Visitor, config, source_code)
        assert actual == problems_expected
