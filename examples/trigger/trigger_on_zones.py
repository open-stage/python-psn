#! /bin/env python
"""
    Complete x,y sACN trigger.
    Trigger script.
"""

import math
import sacn
import pypsn

sender = sacn.sACNsender()
zones = []
settings = {}
settings["universe"] = 1
settings["ip_addr"] = "10.0.0.1"
settings["radius"] = 1.00
settings["min_distance"] = 0.70


def start_dmx():
    """
        Start DMX sender thread.
    """
    universe = settings["universe"]
    sender.start()  # start the sending thread
    sender.activate_output(universe)  # start sending data in 1st universe
    sender[universe].multicast = True  # set multicast to True


def stop_dmx():
    """
        Stop DMX sender thread.
    """
    sender.stop()  # do not forget to stop the sender


def set_settings_from_file(settings):
    """
        Update global settings from file.

    """
    try:
        with open("settings.txt", encoding="UTF-8") as uni_lines:
            for uni_line in uni_lines.readlines():
                uni_line = str(uni_line).strip()
                if len(uni_line) < 1 or uni_line[1] == "#":
                    continue
                if "universe" in uni_line:
                    settings["universe"] = int(uni_line.split(":")[1].strip())
                elif "ip_addr" in uni_line:
                    settings["ip_addr"] = uni_line.split(":")[1].strip()
                elif "min_distance" in uni_line:
                    settings["min_distance"] = float(
                        uni_line.split(":")[1].strip()
                    )
                elif "radius" in uni_line:
                    settings["radius"] = float(uni_line.split(":")[1].strip())
        print("got these settings", settings)
    except Exception as e:
        print("Settings not imported, error was:", e)


def set_zones_from_file(zones):
    """
        Update zones from file.

    Args:
        zones (list): zone coordinates
    """
    try:
        with open("zones.txt", encoding="UTF-8") as zone_lines:
            for zone_line in zone_lines.readlines():
                zone_line = str(zone_line).strip()
                if len(zone_line) < 5:
                    continue
                zone_x, zone_y = zone_line.split(",")
                zones.append((float(zone_x), float(zone_y)))
        print("New zones", zones)
    except Exception as e:
        zones = []
        print("Zones not imported from zones.txt. Error was:", e)


def start_psn():
    """
        Start PSN receiver thread.

    Returns:
        Receiver: psn receiver class
    """
    pypsn.Receiver(check_zones, settings["ip_addr"]).start()


def check_zones(psn_data):
    """
        Update global coordinates.

    Args:
        psn_data (psnDataPacket): psn data class
    """
    if isinstance(psn_data, pypsn.PsnDataPacket):
        x, _, y = psn_data.trackers[0].pos
        radius = settings["radius"]
        min_distance = settings["min_distance"]
        pos = [x, y]
        mult = 255 / radius
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
            print(idx, pos, zone, distance, value)
            dmx_data[idx] = value

        sender[settings["universe"]].dmx_data = dmx_data


if __name__ == "__main__":
    set_zones_from_file(zones)
    set_settings_from_file(settings)
    start_dmx()
    start_psn()
