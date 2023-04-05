#! /bin/env python
import pypsn
import binascii
from time import sleep


def main_local():
    with open("data.log") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip().replace("b'", "").replace("'", "")
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn.parse_psn_packet(hexdata)
            if isinstance(data, pypsn.psn_data_packet):
                print(data.trackers[0].pos)


def main_local_dmx(callback):
    with open("data.log") as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip().replace("b'", "").replace("'", "")
            # print(psn_line)
            hexdata = binascii.unhexlify(psn_line)
            psn_data = pypsn.parse_psn_packet(hexdata)
            if isinstance(psn_data, pypsn.psn_data_packet):
                print(psn_data.trackers[0].pos)
                callback(psn_data)
            sleep(1)  # to have time to observe something...
