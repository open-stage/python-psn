#! /bin/env python3
"""
Usage: python send_psn.py 192.168.1.4 <--- change IP address

"""

import sys
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
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                speed=pypsn.PsnVector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                ori=pypsn.PsnVector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                accel=pypsn.PsnVector3(
                    x=0.0,
                    y=0.0,
                    z=0.0,
                ),
                trgtpos=pypsn.PsnVector3(
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

print("\n--- PSN infos to be sent ---")
print("system name: " + psn_info.name)
print("timestamp: " + str(psn_info.info.timestamp))
print("version_high: " + str(psn_info.info.version_high))
print("version_low: " + str(psn_info.info.version_low))
print("frame_id: " + str(psn_info.info.frame_id))
print("packet_count: " + str(psn_info.info.packet_count))

for tracker in psn_info.trackers:
    print(str(tracker.tracker_id) + ": " + str(tracker.tracker_name))

print("\n--- PSN data to be sent ---")
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

psn_info_packet_bytes = pypsn.prepare_psn_info_packet_bytes(psn_info)
psn_data_packet_bytes = pypsn.prepare_psn_data_packet_bytes(psn_data)

pypsn.send_psn_packet(
    psn_packet=psn_info_packet_bytes,
    mcast_ip="236.10.10.10",
    ip_addr=sys.argv[1],
    mcast_port=56565,
)

pypsn.send_psn_packet(
    psn_packet=psn_data_packet_bytes,
    mcast_ip="236.10.10.10",
    ip_addr=sys.argv[1],
    mcast_port=56565,
)
