# python-psn

Python only parsing library for PSN V2 - [PosiStageNet](https://posistage.net/)

PSN specification as per [GitHub repo](https://github.com/vyv/psn-cpp/blob/master/doc/PosiStageNetprotocol_v2.03_2019_09_09.pdf)

## Installation

To install from git, run pip:
```python
python -m pip install https://codeload.github.com/open-stage/python-psn/zip/refs/heads/master
```

## Usage

```python
import pypsn

# define a callback function
def callback_function(data):
    if isinstance(data, pypsn_module.psn_data_packet): # packet type: psn.psn_data_packet
        for tracker in data.trackers: # loop through all trackers
            print(tracker.pos) # print the received coordinates

    if isinstance(data, pypsn_module.psn_info_packet): # packet type: psn.psn_info_packet
        print(data.name) # print server name
        for tracker in data.trackers: # loop through all trackers
            print(tracker.tracker_name) # print the received tracker name

# provide a callback function and an IP address
receiver = pypsn.receiver(callback_function, "10.0.0.1")
receiver.start()  # start the receiving thread

receiver.stop() # stop receiving

```
See examples folder for some more examples. 

## Development, status

- Supporting PSN V2
- Parsing only, not sending
- Using threading module
- Linux, Windows and macOS tested
- Typed
- Initial pytest testing provided together with CI/CD setup

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
