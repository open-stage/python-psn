#! /bin/env python3
# MIT License
#
# Copyright (C) 2024 Matthew Franklin, vanous
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
Usage: python receive_psn.py 192.168.1.11 <--- change IP address
"""

import sys
import pypsn


def callback(psn_data):
    """
        PSN data reception callback.

    Args:
        psn_data (psnDataPacket): psn data class
    """
    try:
        system_name = str(psn_data.name)

        print("--- Recieved PSN infos ---")
        print("system name: " + system_name)
        print("timestamp: " + str(psn_data.info.timestamp))
        print("version_high: " + str(psn_data.info.version_high))
        print("version_low: " + str(psn_data.info.version_low))
        print("frame_id: " + str(psn_data.info.frame_id))
        print("packet_count: " + str(psn_data.info.packet_count))

        for tracker in psn_data.trackers:
            print(str(tracker.tracker_id) + ": " + str(tracker.tracker_name))

    except Exception:
        print("--- Recieved PSN data ---")

        print("timestamp: " + str(psn_data.info.timestamp))
        print("version_high: " + str(psn_data.info.version_high))
        print("version_low: " + str(psn_data.info.version_low))
        print("frame_id: " + str(psn_data.info.frame_id))
        print("packet_count: " + str(psn_data.info.packet_count))

        for tracker in psn_data.trackers:
            print(
                "tracker ID: "
                + str(tracker.tracker_id)
                + " tracker info: "
                + str(tracker.info)
                + " / "
                + str(tracker.pos)
                + " / "
                + str(tracker.speed)
                + " / "
                + str(tracker.ori)
                + " / "
                + str(tracker.accel)
                + " / "
                + str(tracker.trgtpos)
                + " / "
                + str(tracker.status)
                + " / "
                + str(tracker.timestamp)
            )


pypsn.Receiver(callback, sys.argv[1]).start()
