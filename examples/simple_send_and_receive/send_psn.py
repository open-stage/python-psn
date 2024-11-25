#! /bin/env python3
import sys
import pypsn

# Usage: python send_psn.py 192.168.1.4 <--- change IP address to used interface

psn_info = pypsn.psn_info_packet(
    info=pypsn.psn_info(
        timestamp=1312,
        version_high=2,
        version_low=0,
        frame_id=56,
        packet_count=1,
    ),
    name='system_name_001',
    trackers=(
        [
            pypsn.psn_tracker_info(
                tracker_id=i,
                tracker_name="tracker_" + str(i),
            ) for i in range(0, 7)
        ]
    )
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
            ) for tracker in psn_info.trackers
        ]
    )
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

psn_info_packet_bytes = pypsn.prepare_psn_info_packet_bytes(psn_info)
psn_data_packet_bytes = pypsn.prepare_psn_data_packet_bytes(psn_data)

pypsn.send_psn_packet(
    psn_packet=psn_info_packet_bytes,
    mcast_ips=['236.10.10.10'],
    ip_addr=sys.argv[1],
    mcast_port=56565,
)

pypsn.send_psn_packet(
    psn_packet=psn_data_packet_bytes,
    mcast_ips=['236.10.10.10'],
    ip_addr=sys.argv[1],
    mcast_port=56565,
)

