# python-psn

Pure Python parsing library for PSN V2 - [PosiStageNet](https://posistage.net/)

[Official PSN specification](https://github.com/vyv/psn-cpp/blob/master/doc/PosiStageNetprotocol_v2.03_2019_09_09.pdf)

[Source code](https://github.com/open-stage/python-psn)

[PyPi page](https://pypi.org/project/pypsn/)

[![Pytest](https://github.com/open-stage/python-psn/actions/workflows/run-tests.yaml/badge.svg)](https://github.com/open-stage/python-psn/actions/workflows/run-tests.yaml)

[![Check links in markdown](https://github.com/open-stage/python-psn/actions/workflows/check-links.yaml/badge.svg)](https://github.com/open-stage/python-psn/actions/workflows/check-links.yaml)

## Installation

```bash
pip install pypsn
```

To install latest master from git via pip:
```bash
python -m pip install https://codeload.github.com/open-stage/python-psn/zip/refs/heads/master
```

## Usage

### Receiving PSN data
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
receiver = pypsn.receiver(callback_function)
receiver.start()  # start the receiving thread

receiver.stop() # stop receiving

```

### Senfing PSN data
```python
import pypsn

# create a psn_info object with appropriate data
psn_info = pypsn.PsnInfoPacket(
    info=pypsn.PsnInfo(
        timestamp=1312,
        version_high=2,
        version_low=0,
        frame_id=1,
        packet_count=1,
    ),
    name="system_name_001",
    trackers=(
        [
            pypsn.PsnTrackerInfo(
                tracker_id=i,
                tracker_name="tracker_" + str(i),
            )
            for i in range(0, 8))
        ]
    ),
)

# convert the object to a byte string
psn_info_packet_bytes = pypsn.prepare_psn_info_packet_bytes(psn_info)

# send the PSN info via multicast
pypsn.send_psn_packet(
    psn_packet=psn_info_packet_bytes,
    mcast_ip="236.10.10.10",
    ip_addr="192.168.1.42",
    mcast_port=56565,
)

```
See examples folder for some more examples.

## Development, status

- Supporting PSN V2
- Parsing and sending (via [Multicast Expert](https://github.com/multiplemonomials/multicast_expert)) or via Unicast
- Using threading module
- Linux (Rpi OS incl.), Windows and macOS tested
- PSN messages recognized by GrandMa3 2.1
- Typed, no-strict
- Initial pytest testing provided together with CI/CD setup

### Type hints

* At this point, the `--no-strict-optional` is needed for mypy tests to pass:

```bash
mypy pypsn/*py  --pretty  --no-strict-optional
```
### Format

- To format, use [ruff](https://docs.astral.sh/ruff/)

### Testing

- to test, use `pytest`
- to test typing with mypy use

```bash
pytest --mypy -m mypy pypsn/*py
```

