"""Tests for the plugin module."""
# pylint: disable=no-self-use,protected-access,too-few-public-methods
import ast
import json
from pathlib import Path

import pytest
from _pytest.mark.structures import ParameterSet

from flake8_plus.config import Config
from flake8_plus.visitors.plu001_visitor import PLU001Visitor, _build_message


def _generate_bulk_cases() -> list[ParameterSet]:  # pylint: disable=too-many-locals
    case_files_folder = Path(__file__).parent.parent / "case_files" / "plu001"
    file_dicts = json.load((case_files_folder / "cases.json").open())
    cases: list[ParameterSet] = []
    for file_dict in file_dicts:
        filename = case_files_folder / file_dict["filename"]
        code = filename.read_text(encoding="utf-8")
        for case_dict in file_dict["cases"]:
            blanks_expected = case_dict["blanks_expected"]
            raw_problems = case_dict["problems"]
            problems = set()
            for raw_problem in raw_problems:
                line = raw_problem["line"]
                col = raw_problem["col"]
                blanks_before = raw_problem["blanks_before"]
                message = _build_message(blanks_before, blanks_expected)
                problem = f"{line}:{col} PLU001 {message}"
                problems.add(problem)
            id_ = f"({blanks_expected}) " + " ".join(filename.stem.split("_"))
            case = pytest.param(code, blanks_expected, problems, id=id_)
            cases.append(case)
    return cases


def _results(code: str, blanks_before_imports: int) -> set[str]:
    lines = code.split("\n")
    config = Config(blanks_before_imports)
    visitor = PLU001Visitor(lines, config)
    tree = ast.parse(code)
    visitor.visit(tree)
    messages = set(
        f"{p.line_number}:{p.col_offset+1} {p.formatted_message}"
        for p in visitor.problems
    )
    return messages


class TestPLU001Visitor:
    """Tests for the `PLU001Visitor` class."""

    @pytest.mark.parametrize(
        ("code", "blanks_before_imports", "expected"),
        _generate_bulk_cases(),
    )
    def test_bulk(self, code: str, blanks_before_imports: int, expected: set[str]):
        """Run bulk test cases."""
        actual = _results(code, blanks_before_imports)
        assert actual == expected
