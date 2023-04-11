# python-psn

Python only parsing library for PSN - [PosiStageNet](https://posistage.net/)

PSN specification as per [GitHub repo](https://github.com/vyv/psn-cpp/blob/master/doc/PosiStageNetprotocol_v2.03_2019_09_09.pdf)

## Installation

To install from git, run pip:
```python
python -m pip install https://codeload.github.com/open-stage/python-psn/zip/refs/heads/master
```

## Usage

```python
import pypsn

def callback_function(data):
    if isinstance(data, pypsn_module.psn_data_packet):
        print(data.trackers[0].pos)

    if isinstance(data, pypsn_module.psn_info_packet):
        print(data.name)
        print(data.trackers[0].tracker_name)

pypsn.receiver(callback_function, "10.0.0.1").start()

```
See examples folder for some implementation examples. 

## Status

- Currently implemented:
    - PSN V2
    - Parsing
    - Callback for data packet

### Type hints

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


