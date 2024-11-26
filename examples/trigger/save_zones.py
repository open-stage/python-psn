#! /bin/env python
"""
Complete x,y sACN trigger.
Callibration script.
"""

import pypsn

X = 0
Y = 0
Z = 0


def set_settings_from_file(old_settings):
    """
    Update global settings from file.

    """
    try:
        new_settings = old_settings.copy()
        with open("settings.txt", encoding="UTF-8") as uni_lines:
            for uni_line in uni_lines.readlines():
                uni_line = str(uni_line).strip()
                if len(uni_line) < 1 or uni_line[1] == "#":
                    continue
                if "universe" in uni_line:
                    new_settings["universe"] = int(uni_line.split(":")[1].strip())
                elif "ip_addr" in uni_line:
                    new_settings["ip_addr"] = uni_line.split(":")[1].strip()
                elif "min_distance" in uni_line:
                    new_settings["min_distance"] = float(uni_line.split(":")[1].strip())
                elif "radius" in uni_line:
                    new_settings["radius"] = float(uni_line.split(":")[1].strip())
        print("got these settings", new_settings)
        return new_settings
    except Exception as e:
        print("Settings not imported, error was:", e)
        return old_settings


def start_psn(ip_addr):
    """
        Start PSN receiver thread.

    Returns:
        Receiver: psn receiver class
    """
    receiver = pypsn.Receiver(check_zones, ip_addr, timeout=2)
    receiver.start()
    return receiver


def check_zones(psn_data):
    """
        Update global coordinates.

    Args:
        psn_data (psnDataPacket): psn data class
    """
    if isinstance(psn_data, pypsn.PsnDataPacket):
        global X, Y, Z
        print(psn_data.trackers[0].pos)
        X, Y, Z = psn_data.trackers[0].pos


def set_zones_from_file(old_zones):
    """
        Update zones from file.

    Args:
        zones (list): zone coordinates
    """
    try:
        new_zones = old_zones
        with open("zones.txt", "r", encoding="UTF-8") as zone_lines:
            for zone_line in zone_lines.readlines():
                zone_line = str(zone_line).strip()
                if len(zone_line) < 5:
                    continue
                zone_x, zone_y = zone_line.split(",")
                new_zones.append((float(zone_x), float(zone_y)))
        print("New zones", new_zones)
        return new_zones
    except Exception as e:
        print(
            "Zones not imported from zones.txt, " + "using default ones. Error was:", e
        )
        return old_zones


def set_zones_to_file(zones):
    """
        Update zones to file.

    Args:
        zones (list): zone coordinates
    """
    try:
        with open("zones.txt", "w", encoding="UTF-8") as zone_lines:
            for zone in zones:
                zone_lines.write(f"{zone[0]},{zone[1]}\n")
    except Exception as e:
        print("Zone file could not be written...", e)


if __name__ == "__main__":
    glob_settings = {}
    glob_settings["universe"] = 1
    glob_settings["ip_addr"] = "10.0.0.1"
    glob_settings["radius"] = 1.00
    glob_settings["min_distance"] = 0.70

    glob_zones = []

    glob_zones = set_zones_from_file(glob_zones)
    glob_settings = set_settings_from_file(glob_settings).copy()
    glob_receiver = start_psn(glob_settings.get("ip_addr"))

    while True:
        val = input("Press enter to store current position as a zone, press q to Quit")
        if val.lower() == "q":
            glob_receiver.stop()
            break
        print(f"Save {X}, {Y}, number of zones: {len(glob_zones)}")
        glob_zones.append((X, Y))
        set_zones_to_file(glob_zones)
