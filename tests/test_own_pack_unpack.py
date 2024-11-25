import binascii
import pypsn
from pathlib import Path
# Test packing and parsing our own data


psn_info = pypsn.psn_info_packet(
    info=pypsn.psn_info(
        timestamp=1312,
        version_high=2,
        version_low=0,
        frame_id=56,
        packet_count=1,
    ),
    name="system_name_001",
    trackers=(
        [
            pypsn.psn_tracker_info(
                tracker_id=i,
                tracker_name="tracker_" + str(i),
            )
            for i in range(0, 7)
        ]
    ),
)
psn_data = pypsn.psn_data_packet(
    info=psn_info.info,
    trackers=(
        [
            pypsn.psn_tracker(
                id=tracker.tracker_id,
                info=psn_info.info,
                pos=pypsn.psn_vector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                speed=pypsn.psn_vector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                ori=pypsn.psn_vector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                accel=pypsn.psn_vector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                trgtpos=pypsn.psn_vector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                status=0,
                timestamp=psn_info.info.timestamp,
            )
            for tracker in psn_info.trackers
        ]
    ),
)


def get_test_data():
    return pypsn.prepare_psn_data_packet_bytes(psn_data)


def get_test_info():
    return pypsn.prepare_psn_info_packet_bytes(psn_info)


def test_data_data(pypsn_module):
    """Test position"""
    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    test_vector = pypsn_module.psn_vector3(0.0, 0.0, 0.0)
    if isinstance(data, pypsn_module.psn_data_packet):
        assert test_vector == data.trackers[0].pos


def test_data_info(pypsn_module):
    """Test header info data"""

    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    if isinstance(data, pypsn_module.psn_data_packet):
        assert 56 == data.info.frame_id
        assert 1 == data.info.packet_count
        assert 1312 == data.info.timestamp
        assert 2 == data.info.version_high
        assert 0 == data.info.version_low


def test_info_info(pypsn_module):
    """Test header info data and system name"""

    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    if isinstance(data, pypsn_module.psn_info_packet):
        assert b"system_name_001" == data.name
        assert 56 == data.info.frame_id
        assert 1 == data.info.packet_count
        assert 1312 == data.info.timestamp
        assert 2 == data.info.version_high
        assert 0 == data.info.version_low


def test_info_data(pypsn_module):
    """Test tracker name"""

    hexdata = get_test_info()
    data = pypsn_module.parse_psn_packet(hexdata)
    if isinstance(data, pypsn_module.psn_info_packet):
        assert data.trackers[0].tracker_name == b"tracker_0"
