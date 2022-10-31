# Flake8-plus

[![CircleCI](https://dl.circleci.com/status-badge/img/gh/sorenlind/flake8-plus/tree/main.svg?style=shield)](https://dl.circleci.com/status-badge/redirect/gh/sorenlind/flake8-plus/tree/main)
[![codecov](https://img.shields.io/codecov/c/github/sorenlind/flake8-plus?token=8ULWSRBPNC)](https://codecov.io/gh/sorenlind/flake8-plus)
[![license](https://black.readthedocs.io/en/stable/_static/license.svg)](https://github.com/sorenlind/flake8-plus/blob/main/LICENSE)
[![pypi](https://img.shields.io/pypi/v/flake8-plus)](https://pypi.org/project/flake8-plus/)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Flake8-plus is a plugin for [Flake8](https://github.com/PyCQA/flake8) that detects
incorrect amounts of vertical whitespace before the first toplevel `import` statement,
before `return` statements and before `except`. The plugin can be configured to expect
any number of blank lines. By default, the plugin expects no blank lines before both the
`import` and `return` statements, and the `except` keyword.

## Installation

Flake8-plus can be installed from PyPI using `pip`:

```shell
$ pip install flake8-plus
```

You can verify that it has been installed as follows (the version numbers you see may
vary):

```shell
$ flake8 --version
5.0.4 (flake8-plus: 0.1.0, mccabe: 0.7.0, pycodestyle: 2.9.1, pyflakes: 2.5.0)
```

## Configuration

You can set the required number of blank lines before the first `import` as well as the
number of blank lines required before a `return` and before `except`. This can be done
from the command line:

```shell
$ flake8 --blanks-before-imports 1 --blanks-before-return 1 --blanks-before-except 1
```

Or from one of the `setup.cfg`, `tox.ini`, or `.flake8` files:

```ini
[flake8]
blanks-before-imports=1
blanks-before-return=1
blanks-before-except=1
```

## Why no blank lines?

### Before `import`

Neither [Black](https://github.com/psf/black), [Flake8](https://github.com/PyCQA/flake8)
nor [Pylint](https://github.com/PyCQA/pylint) enforces a specific number of blank lines
preceding the first `import` and consequently there seems to be no consensus or
standard. The table below shows the frequency of the number of blank lines before the
first toplevel `import` statement in the code bases for Black, Flake8 and Pylint (as of
October 2022).

| Package | Total files | 0 blanks | 1 blank | 2 blanks | Folder        |
| ------- | ----------: | -------: | ------: | -------: | ------------- |
| Black   |          33 |       21 |      12 |        0 | `src`         |
| Flake8  |          32 |       32 |       0 |        0 | `src/flake8/` |
| Pylint  |         177 |        3 |     170 |        4 | `pylint`      |

Clearly, there is no real consensus. Black seems undecided, Flake8 consistently uses 0
blanks, and Pylint seems to prefer 1 blank line. However, it's worth noting that the
Pylint code does not consistently include module docstrings (thereby breaking
`pylint(missing-module-docstring)`). For that reason, and also because this is a Flake8
plugin, the plugin follows the style of Flake8 as the default.

### Before `return`

Neither Black, Flake8 nor Pylint enforces a specific number of blank lines preceding
`return`. However, they all use zero blank lines more frequently than they use any
other number of blanks. The table below shows the frequency of the number of blank
lines before a `return` statement in the code bases for Black, Flake8 and Pylint (as of
October 2022).

| Package | Total `return`s | 0 blanks | 1 blank | 2 blanks | Folder        |
| ------- | --------------: | -------: | ------: | -------: | ------------- |
| Black   |             618 |      544 |      74 |        0 | `src`         |
| Flake8  |             174 |      155 |      19 |        0 | `src/flake8/` |
| Pylint  |            1941 |     1852 |      89 |        0 | `pylint`      |

Since zero blank lines is the style used most frequently, Flake8-plus uses that as that
as the default.

### Before `except`

Neither Black, Flake8 nor Pylint enforces a specific number of blank lines preceding
`except`. However, they all use zero blank lines more frequently than they use any other
number of blanks. The table below shows the frequency of the number of blank lines
before an `except` statement in the code bases for Black, Flake8 and Pylint (as of
October 2022).

| Package | Total `except`s | 0 blanks | 1 blank | 2 blanks | Folder        |
| ------- | --------------: | -------: | ------: | -------: | ------------- |
| Black   |              71 |       64 |       7 |        0 | `src`         |
| Flake8  |              26 |       26 |       0 |        0 | `src/flake8/` |
| Pylint  |             285 |      283 |       2 |        0 | `pylint`      |

Since zero blank lines is the style used most frequently, Flake8-plus uses that as that
as the default.

## Reported problems

| Code   |  Description                                                |
| ------ | ----------------------------------------------------------- |
| PLU001 | "expected {} blank lines before first import, found {}"     |
| PLU002 | "expected {} blank lines before return statement, found {}" |
| PLU003 | "expected {} blank lines before except, found {}"           |
