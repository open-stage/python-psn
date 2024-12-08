#! /bin/env python3
"""
Usage:

multicast: python send_psn.py 1 192.168.1.4 236.10.10.10
unicast: python send_psn.py 1 192.168.1.4

Args:
- number of trackers to generate
- local IP adress
- multricast adress (opt)

Variables mapping for GrandMa3 users:

- pos.xyz -> Position X Y Z
- speed.xyz -> Speed X Y Z
- ori.xyz -> Rot X Y Z
- accel.xyz -> None
- trgtpos.xyz -> None

"""

import sys
import time
import pypsn

try:
    tracker_num = int(sys.argv[1])
    ip_addr = sys.argv[2]
    mcast_ip = None

    if sys.argv[3]:
        mcast_ip = sys.argv[3]

except Exception as e:
    print("Args: tracker_num ip_addr mcast_ip (opt).")
    print(e)

start_time_us = time.time_ns() // 1000

psn_info = pypsn.PsnInfoPacket(
    info=pypsn.PsnInfo(
        timestamp=start_time_us,
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
            for i in range(0, tracker_num)
        ]
    ),
)

psn_data = pypsn.PsnDataPacket(
    info=pypsn.PsnInfo(
        timestamp=start_time_us,
        version_high=2,
        version_low=0,
        frame_id=1,
        packet_count=1,
    ),
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
                status=0.5,
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
                timestamp=start_time_us,
            )
            for tracker in psn_info.trackers
        ]
    ),
)

print("\n--- PSN infos to be sent at 1Hz ---")
print("system name: " + psn_info.name)
print("timestamp: " + str(psn_info.info.timestamp))
print("version_high: " + str(psn_info.info.version_high))
print("version_low: " + str(psn_info.info.version_low))
print("frame_id: " + str(psn_info.info.frame_id))
print("packet_count: " + str(psn_info.info.packet_count))

for tracker in psn_info.trackers:
    print(str(tracker.tracker_id) + ": " + str(tracker.tracker_name))

print("\n--- PSN data to be sent at 60Hz ---")
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

print("\n--- Sendin PSN data in loop ---")
counter = 0.0

while True:
    time.sleep(1 / 60)
    elapsed_time_us = time.time_ns() // 1000 - start_time_us

    if counter < 6.0:
        counter += 0.1
    else:
        counter = 0.0

        psn_info.info.timestamp = elapsed_time_us
        psn_info_packet_bytes = pypsn.prepare_psn_info_packet_bytes(psn_info)

        pypsn.send_psn_packet(
            psn_packet=psn_info_packet_bytes,
            mcast_ip=mcast_ip,
            ip_addr=ip_addr,
            port=56565,
        )

    psn_data.info.timestamp = elapsed_time_us

    if psn_data.info.frame_id < 255:
        psn_data.info.frame_id += 1
    else:
        psn_data.info.frame_id = 0

    for tracker in psn_data.trackers:
        tracker.timestamp = elapsed_time_us
        tracker.pos.x = counter
        tracker.speed.x = counter
        tracker.ori.x = counter
        tracker.accel.x = counter
        tracker.trgtpos.x = counter

    psn_data_packet_bytes = pypsn.prepare_psn_data_packet_bytes(psn_data)

    pypsn.send_psn_packet(
        psn_packet=psn_data_packet_bytes,
        mcast_ip=mcast_ip,
        ip_addr=ip_addr,
        port=56565,
    )
