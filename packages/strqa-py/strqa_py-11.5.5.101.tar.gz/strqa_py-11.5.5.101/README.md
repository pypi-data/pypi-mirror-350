![Strategy One Logo][logo]

# StrQA: Test Center for Strategy One

`strqa-py` allows [Strategy One](https://www.strategysoftware.com/strategyone) administrators to automate integrity tests and validate that their data remains consistent and accurate after changes such like upgrades, warehouse migrations, or maintenance tasks.

This package provides tools to:
- Create a baseline file specifying properties of specified objects in a Strategy One environment.
- Compare properties of objects between two projects or environments.

![Example output][example_summary]

# Usage

This package is to be used with Strategy One and the [mstrio-py](https://pypi.org/project/mstrio-py) package.

```python
strqa = StrQA(
    objects=[OlapCube(...), ...],
    path='path/to/results',
)
result = strqa.project_vs_project(target_connection=target_conn)
```
This will create HTML files with the test report.

For details, see examples in the `code_snippets` folder.

# Installation

## Prerequisites

- Python 3.10+
- Strategy One 2021+
This package uses [mstrio-py][mstrio_pypi]. It will be installed automatically when installing `strqa-py`.

## Install the `strqa-py` Package

Install with [pip][strqa_pypi]:

```bash
pip install strqa-py
```

It is recommended to install and run `strqa-py` in Python's [virtual environment][python_venv].


[logo]: https://github.com/MicroStrategy/mstrio-py/blob/master/strategy-logo.png?raw=true
[example_summary]: ./example-summary.png
[mstrio_pypi]: https://pypi.org/project/mstrio-py
[strqa_pypi]: https://pypi.org/project/strqa-py
[python_venv]: https://docs.python.org/3/tutorial/venv.html
