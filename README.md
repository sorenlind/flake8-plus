# Flake8-plus

Flake8-plus is a plugin for [Flake8](https://github.com/PyCQA/flake8) that detects
incorrect amounts of vertical whitespace before the first toplevel `import` statement.
By default, the plugin issues a warning if there are blank lines immediately preceding
the first toplevel `import`. The plugin can be configured to expect any number of blank
lines.

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

You can set the required number of blank lines before the first `import`. This can be
done from the command line:

```shell
$ flake8 --blanks-before-imports 1
```

Or from one of the `setup.cfg`, `tox.ini`, or `.flake8` files:

```ini
[flake8]
blanks-before-imports=1
```

## Why no blank lines?

Neither Black, Flake8 nor Pylint enforces a specific number of blank lines preceding the
first `import` and consequently there seems to be no consensus or standard. The table
below shows the frequency of the number of blank lines before the first toplevel
`import` statement in the code bases for [Black](https://github.com/psf/black),
[Flake8](https://github.com/PyCQA/flake8) and [Pylint](https://github.com/PyCQA/pylint)
(as of October 2022).

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

## Reported problems

| Code   |  Description                                            |
| ------ | ------------------------------------------------------- |
| PLU001 | "expected {} blank lines before first import, found {}" |
