#! /bin/env python3
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
                + str(tracker.id)
                + " tracker info: "
                + str(tracker.info)
                + " / " + str(tracker.pos)
                + " / " + str(tracker.speed)
                + " / " + str(tracker.ori)
                + " / " + str(tracker.accel)
                + " / " + str(tracker.trgtpos)
                + " / " + str(tracker.status)
                + " / " + str(tracker.timestamp)
            )


pypsn.Receiver(callback, sys.argv[1]).start()
