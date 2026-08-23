#!/bin/env python3
# MIT License
#
# Copyright (C) 2023 Matthew Franklin, vanous
#
# This file is part of pypsn.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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
