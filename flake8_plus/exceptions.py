"""Exceptions."""


class Flake8PlusError(Exception):
    """Base Flake8-plus exception."""


class MultipleStatementsError(Flake8PlusError):
    """Exception raised when multiple statements are found on one line."""
