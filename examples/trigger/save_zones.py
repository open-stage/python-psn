#! /bin/env python
import pypsn

settings = {}
settings["universe"] = 1
settings["ip_addr"] = "10.0.0.1"
settings["radius"] = 1.00
settings["min_distance"] = 0.70
zones = []

x = 0
y = 0
z = 0


def set_settings_from_file(settings):
    try:
        with open("settings.txt") as uni_lines:
            for uni_line in uni_lines.readlines():
                uni_line = str(uni_line).strip()
                if len(uni_line) < 1 or uni_line[1] == "#":
                    continue
                if "universe" in uni_line:
                    settings["universe"] = int(uni_line.split(":")[1].strip())
                elif "ip_addr" in uni_line:
                    settings["ip_addr"] = uni_line.split(":")[1].strip()
                elif "min_distance" in uni_line:
                    settings["min_distance"] = float(uni_line.split(":")[1].strip())
                elif "radius" in uni_line:
                    settings["radius"] = float(uni_line.split(":")[1].strip())
        print("got these settings", settings)
    except Exception as e:
        print("Settings not imported, error was:", e)


def start_psn():
    receiver = pypsn.receiver(check_zones, settings["ip_addr"], timeout=2)
    receiver.start()
    return receiver


def check_zones(psn_data):
    if isinstance(psn_data, pypsn.psn_data_packet):
        global x, y, z
        print(psn_data.trackers[0].pos)
        x, z, y = psn_data.trackers[0].pos


def set_zones_from_file(zones):
    try:
        with open("zones.txt", "r") as zone_lines:
            for zone_line in zone_lines.readlines():
                zone_line = str(zone_line).strip()
                if len(zone_line) < 5:
                    continue
                zone_x, zone_y = zone_line.split(",")
                zones.append((float(zone_x), float(zone_y)))
        print("New zones", zones)
    except Exception as e:
        print("Zones not imported from zones.txt, using default ones. Error was:", e)


def set_zones_to_file(zones):
    try:
        with open("zones.txt", "w") as zone_lines:
            for zone in zones:
                zone_lines.write(f"{zone[0]},{zone[1]}\n")
    except Exception as e:
        print("Zone file could not be written...", e)


if __name__ == "__main__":
    set_zones_from_file(zones)
    set_settings_from_file(settings)
    receiver = start_psn()
    while True:
        val = input("Press enter to store current position as a zone, press q to Quit")
        if val.lower() == "q":
            receiver.stop()
            break
        print(f"Save {x}, {y}, number of zones: {len(zones)}")
        zones.append((x, y))
        set_zones_to_file(zones)
