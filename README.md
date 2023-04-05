# python-psn

Quick and dirty rudimentary Python parsing library for PSN - [PosiStageNet](https://posistage.net/)

PSN specification as per [GitHub repo](https://github.com/vyv/psn-cpp/blob/master/doc/PosiStageNetprotocol_v2.03_2019_09_09.pdf)

## Installation

To install from git, run pip:
```python
python -m pip install https://codeload.github.com/open-stage/python-psn/zip/refs/heads/master
```

## Usage

```python
import pypsn
pypsn.main(callback)
```
See examples folder for some implementation examples. 

## Status

- This is a very early version, currently implemented:
    - Parsing

## Development

This is very early stage, TODO: add threading support and improve initial module entry point.

### Typing

* At this point, the `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pypsn/*py  --pretty  --no-strict-optional
```
### Format

- to format, use `black`

### Testing

- to test, use `pytest`
- to test typing with mypy use 

```bash
pytest --mypy -m mypy pypsn/*py
```


