#!/bin/env python3
"""
Test parsing on some real world data.
"""

import binascii
from pathlib import Path


def test_data_data(pypsn_module):
    """Test position"""

    test_data_file_path = Path(Path(__file__).parents[0], "data.log")

    with open(test_data_file_path, encoding="UTF-8") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip()
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn_module.parse_psn_packet(hexdata)
            test_vector = pypsn_module.PsnVector3(
                0.20273426175117493, 6.0, -9.693662643432617
            )
            if isinstance(data, pypsn_module.PsnDataPacket):
                assert test_vector == data.trackers[0].pos


def test_data_info(pypsn_module):
    """Test header info data"""

    test_data_file_path = Path(Path(__file__).parents[0], "data.log")

    with open(test_data_file_path, encoding="UTF-8") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip()
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn_module.parse_psn_packet(hexdata)
            if isinstance(data, pypsn_module.PsnDataPacket):
                assert 56 == data.info.frame_id
                assert 1 == data.info.packet_count
                assert 288058234 == data.info.timestamp
                assert 2 == data.info.version_high
                assert 0 == data.info.version_low


def test_info_info(pypsn_module):
    """Test header info data and system name"""

    test_data_file_path = Path(Path(__file__).parents[0], "data.log")

    with open(test_data_file_path, encoding="UTF-8") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip()
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn_module.parse_psn_packet(hexdata)
            if isinstance(data, pypsn_module.PsnInfoPacket):
                assert b"RoboSpot PSN Server" == data.name
                assert 200 == data.info.frame_id
                assert 1 == data.info.packet_count
                assert 288058568 == data.info.timestamp
                assert 2 == data.info.version_high
                assert 0 == data.info.version_low


def test_info_data(pypsn_module):
    """Test tracker name"""

    test_data_file_path = Path(Path(__file__).parents[0], "data.log")

    with open(test_data_file_path, encoding="UTF-8") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip()
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn_module.parse_psn_packet(hexdata)
            if isinstance(data, pypsn_module.PsnInfoPacket):
                assert data.trackers[0].tracker_name == b"RoboCamera"
