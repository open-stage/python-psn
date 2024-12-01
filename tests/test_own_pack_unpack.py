#!/bin/env python3
"""
Test packing and parsing our own data.
"""

import pypsn


psn_info = pypsn.PsnInfoPacket(
    info=pypsn.PsnInfo(
        timestamp=1312,
        version_high=2,
        version_low=0,
        frame_id=56,
        packet_count=1,
    ),
    name="system_name_001",
    trackers=(
        [
            pypsn.PsnTrackerInfo(
                tracker_id=i,
                tracker_name="tracker_" + str(i),
            )
            for i in range(0, 7)
        ]
    ),
)
psn_data = pypsn.PsnDataPacket(
    info=psn_info.info,
    trackers=(
        [
            pypsn.PsnTracker(
                tracker_id=tracker.tracker_id,
                info=psn_info.info,
                pos=pypsn.PsnVector3(
                    x=1.0,
                    y=1.0,
                    z=1.0,
                ),
                speed=pypsn.PsnVector3(
                    x=1.0,
                    y=1.0,
                    z=1.0,
                ),
                ori=pypsn.PsnVector3(
                    x=1.0,
                    y=1.0,
                    z=1.0,
                ),
                accel=pypsn.PsnVector3(
                    x=1.0,
                    y=1.0,
                    z=1.0,
                ),
                trgtpos=pypsn.PsnVector3(
                    x=1.0,
                    y=1.0,
                    z=1.0,
                ),
                status=0.5,
                timestamp=psn_info.info.timestamp,
            )
            for tracker in psn_info.trackers
        ]
    ),
)


def get_test_data():
    """
        Get test data.

    Returns:
        psn data packet: as bytes
    """
    return pypsn.prepare_psn_data_packet_bytes(psn_data)


def get_test_info():
    """
        Get test info.

    Returns:
        psn data packet: as bytes
    """
    return pypsn.prepare_psn_info_packet_bytes(psn_info)


def test_data_data(pypsn_module):
    """Test position"""
    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    test_vector = pypsn_module.PsnVector3(1.0, 1.0, 1.0)
    if isinstance(data, pypsn_module.PsnDataPacket):
        for tracker_id in range(0, 7):
            assert test_vector == data.trackers[tracker_id].pos
            assert test_vector == data.trackers[tracker_id].ori
            assert test_vector == data.trackers[tracker_id].speed
            assert test_vector == data.trackers[tracker_id].accel
            assert test_vector == data.trackers[tracker_id].trgtpos
            assert 0.5 == data.trackers[tracker_id].status
            assert 1312 == data.trackers[tracker_id].timestamp
            assert tracker_id == data.trackers[tracker_id].tracker_id


def test_data_info(pypsn_module):
    """Test header info data"""

    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    if isinstance(data, pypsn_module.PsnDataPacket):
        assert 56 == data.info.frame_id
        assert 1 == data.info.packet_count
        assert 1312 == data.info.timestamp
        assert 2 == data.info.version_high
        assert 0 == data.info.version_low


def test_info_info(pypsn_module):
    """Test header info data and system name"""

    hexdata = get_test_data()
    data = pypsn_module.parse_psn_packet(hexdata)
    if isinstance(data, pypsn_module.PsnInfoPacket):
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
    if isinstance(data, pypsn_module.PsnInfoPacket):
        for tracker_id in range(0, 7):
            assert tracker_id == data.trackers[tracker_id].tracker_id
            assert ("tracker_" + str(tracker_id)).encode("UTF-8") == data.trackers[
                tracker_id
            ].tracker_name
