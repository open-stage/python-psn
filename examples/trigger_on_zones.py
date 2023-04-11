#! /bin/env python
import sacn
import pypsn
import math

# Sends sACN DMX when PSN coordinates are near or on given coordinates.

sender = sacn.sACNsender()

settings = {}
settings["universe"] = 1
settings["ip_addr"] = "10.0.0.1"

zones = [
    [4.33588981628418, -18.41270637512207],
    [2.6540772914886475, -18.26753044128418],
    [0.18828973174095154, -19.134809494018555],
]


def start_dmx():
    universe = settings["universe"]
    sender.start()  # start the sending thread
    sender.activate_output(universe)  # start sending out data in the 1st universe
    sender[universe].multicast = True  # set multicast to True


def stop_dmx():
    sender.stop()  # do not forget to stop the sender


def start_psn():
    pypsn.receiver(check_zones, settings["ip_addr"]).start()


def check_zones(psn_data):
    if isinstance(psn_data, pypsn.psn_data_packet):
        x, z, y = psn_data.trackers[0].pos  # Some senders/receivers have flipped xyz...
        pos = [x, y]
        radius = 1.00
        mult = 255 / radius
        min_distance = 0.70
        dmx_data = [0] * 512
        for idx, zone in enumerate(zones):
            distance = math.dist(zone, pos) - min_distance
            if distance < 0:
                distance = 0
            value = int(255 - (distance * mult))
            if value < 0:
                value = 0
            if value > 255:
                value = 255
            dmx_data[idx] = value

        sender[settings["universe"]].dmx_data = dmx_data

if __name__ == "__main__":
    start_dmx()
    start_psn()
