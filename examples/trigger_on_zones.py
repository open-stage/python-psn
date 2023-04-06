#! /bin/env python
import sacn
import pypsn
import math

# Note: not tested

sender = sacn.sACNsender()


def start_dmx():
    sender.start()  # start the sending thread
    sender.activate_output(1)  # start sending out data in the 1st universe
    sender[1].multicast = True  # set multicast to True


def stop_dmx():
    sender.stop()  # do not forget to stop the sender


def start_psn():
    pypsn.receiver(check_zones, "192.168.20.177").start()


def check_zones(psn_data):
    zones = [[1, 1], [2, 2], [3, 3]]
    x, y, z = psn_data.trackers[0].pos
    pos = [x, y]
    radius = 100
    mult = 255 / radius
    min_distance = 70
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

    sender[1].dmx_data = dmx_data


if __name__ == "__main__":
    start_dmx()
    start_psn()
