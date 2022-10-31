"""Test for the `visitors` package."""
# pylint: disable=too-many-locals
import ast
import json
from pathlib import Path

import pytest
from _pytest.mark.structures import ParameterSet

from flake8_plus.config import Config
from flake8_plus.problem import Problem
from flake8_plus.visitors.base_visitor import BaseVisitor


def generate_bulk_cases(problem_cls: type[Problem]) -> list[ParameterSet]:
    """
    Generate bulk test cases for specified `Problem` subclass.

    Args:
        problem_cls (type[Problem]): The problem class to generate test cases for.

    Returns:
        list[ParameterSet]: List of pytest cases.
    """
    case_files_folder = (
        Path(__file__).parent.parent / "case_files" / problem_cls.code.lower()
    )
    file_dicts = json.load((case_files_folder / "cases.json").open())
    cases: list[ParameterSet] = []
    for file_dict in file_dicts:
        filename = case_files_folder / file_dict["filename"]
        code = filename.read_text(encoding="utf-8")
        for case_dict in file_dict["cases"]:
            expectation = case_dict["expectation"]
            problems = set()
            for problem_dict in case_dict["problems"]:
                problem = problem_cls(**problem_dict, **expectation)
                problems.add(_problem_to_tuple(problem))
            exp = ", ".join([f"{v} {k}" for (k, v) in expectation.items()])
            id_ = f"{filename.stem} - {exp}".replace("_", " ")
            case = pytest.param(code, expectation, problems, id=id_)
            cases.append(case)
    return cases


def generate_results(
    visitor_cls: type[BaseVisitor], config: Config, source_code: str
) -> set[tuple[int, int, str]]:
    """
    Generate results for specified `BaseVisitor` subclass on specified source code.

    Args:
        visitor_cls (type[BaseVisitor]): The visitor to use for generating results.
        source_code (str): The source code to check.
        blanks_before_imports (int): _description_

    Returns:
        set[tuple[int, int, str]]: A set of problems as tuples.
    """
    lines = source_code.split("\n")
    visitor = visitor_cls(lines, config)
    tree = ast.parse(source_code)
    visitor.visit(tree)
    messages = set(_problem_to_tuple(p) for p in visitor.problems)
    return messages


def _problem_to_tuple(problem: Problem) -> tuple[int, int, str]:
    return (
        problem.line_number,
        problem.col_offset,
        problem.message_with_code,
    )
