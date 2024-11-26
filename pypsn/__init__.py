#!/bin/env python3
"""
    Pure python PSN interface.
"""

import socket
from struct import pack, unpack
from enum import IntEnum
from typing import List
import os
from threading import Thread
import multicast_expert

__version__ = "0.2.4"


class PsnVector3:
    """_summary_
    """
    def __init__(self, x: float, y: float, z: float):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"{self.x}, {self.y}, {self.z}"

    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __iter__(self):
        return iter((self.x, self.y, self.z))


class PsnInfo:
    """_summary_
    """
    def __init__(
        self,
        timestamp: int,
        version_high: int,
        version_low: int,
        frame_id: int,
        packet_count: int,
    ):
        self.timestamp = timestamp
        self.version_high = version_high
        self.version_low = version_low
        self.frame_id = frame_id
        self.packet_count = packet_count


class PsnTrackerInfo:
    """_summary_
    """
    def __init__(self, tracker_id: int, tracker_name: str):
        self.tracker_id = tracker_id
        self.tracker_name = tracker_name


class PsnTracker:
    """_summary_
    """
    def __init__(
        self,
        tracker_id: int,
        info: "PsnInfo" = None,
        pos: "PsnVector3" = None,
        speed: "PsnVector3" = None,
        ori: "PsnVector3" = None,
        accel: "PsnVector3" = None,
        trgtpos: "PsnVector3" = None,
        status: int = 0,
        timestamp: int = 0,
    ):
        self.tracker_id = tracker_id
        self.info = info
        self.pos = pos
        self.speed = speed
        self.ori = ori
        self.accel = accel
        self.trgtpos: PsnVector3 = trgtpos
        self.status = status
        self.timestamp = timestamp


class PsnDataPacket:
    """_summary_
    """
    def __init__(self, info: "PsnInfo", trackers: List["PsnTracker"]):
        self.info = info
        self.trackers = trackers


class PsnInfoPacket:
    """_summary_
    """
    def __init__(
        self,
        info: "PsnInfo",
        name: str,
        trackers: List["PsnTrackerInfo"],
    ):
        self.info = info
        self.name = name
        self.trackers = trackers


class PsnV1Chunk(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_V1_INFO_PACKET = 0x503C
    PSN_V1_DATA_PACKET = 0x6754


class PsnV2Chunck(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_INFO_PACKET = 0x6756
    PSN_DATA_PACKET = 0x6755


class PsnInfoChunk(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_INFO_PACKET_HEADER = 0x0000
    PSN_INFO_SYSTEM_NAME = 0x0001
    PSN_INFO_TRACKER_LIST = 0x0002


class PsnDataChunk(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_DATA_PACKET_HEADER = 0x0000
    PSN_DATA_TRACKER_LIST = 0x0001


class PasnTrackerListChunk(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_INFO_TRACKER_NAME = 0x0000


class PsnTrackerChunk(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_DATA_TRACKER_POS = 0x0000
    PSN_DATA_TRACKER_SPEED = 0x0001
    PSN_DATA_TRACKER_ORI = 0x0002
    PSN_DATA_TRACKER_ACCEL = 0x0004
    PSN_DATA_TRACKER_TRGTPOS = 0x0005


class PsnTrackerChunkInfo(IntEnum):
    """_summary_

    Args:
        IntEnum (_type_): _description_
    """
    PSN_DATA_TRACKER_STATUS = 0x0003
    PSN_DATA_TRACKER_TIMESTAMP = 0x0006


def join_multicast_windows(mcast_grp, mcast_port, if_ip):
    """_summary_

    Args:
        mcast_grp (_type_): _description_
        mcast_port (_type_): _description_
        if_ip (_type_): _description_

    Returns:
        _type_: _description_
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(mcast_grp) + socket.inet_aton(if_ip),
    )
    sock.bind(("", mcast_port))
    return sock


def join_multicast_posix(mcast_grp, mcast_port, if_ip):
    """_summary_

    Args:
        mcast_grp (_type_): _description_
        mcast_port (_type_): _description_
        if_ip (_type_): _description_

    Returns:
        _type_: _description_
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    try:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as e:
        print(e)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 32)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)

    sock.bind((mcast_grp, mcast_port))
    sock.setsockopt(
        socket.SOL_IP,
        socket.IP_MULTICAST_IF,
        socket.inet_aton(if_ip)
    )
    sock.setsockopt(
        socket.IPPROTO_IP,
        socket.IP_ADD_MEMBERSHIP,
        socket.inet_aton(mcast_grp) + socket.inet_aton(if_ip),
    )
    return sock


def determine_os():
    """_summary_

    Returns:
        _type_: _description_
    """
    if os.name == "nt":
        return str(os.name)

    elif os.name == "posix":
        return str(os.name)

    else:
        return "Operating system not supported"


class Receiver(Thread):
    """_summary_

    Args:
        Thread (_type_): _description_
    """
    def __init__(
        self, callback,
        ip_addr="0.0.0.0",
        mcast_port=56565,
        timeout=2
    ):
        Thread.__init__(self)
        self.callback = callback
        self.running = True
        self.socket = get_socket(ip_addr, mcast_port)
        if timeout is not None and self.socket is not None:
            self.socket.settimeout(timeout)

    def stop(self):
        """_summary_
        """
        self.running = False
        if self.socket is not None:
            self.socket.close()
        self.join()

    def run(self):
        """_summary_
        """
        data = ""
        if self.socket is None:
            return
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1500)
            except Exception as e:
                print("Network data error:", e)
            else:
                psn_data = parse_psn_packet(data)
                self.callback(psn_data)


def get_socket(ip_addr, mcast_port):
    """_summary_

    Args:
        ip_addr (_type_): _description_
        mcast_port (_type_): _description_

    Returns:
        _type_: _description_
    """
    mcast_grp = "236.10.10.10"
    sock = None
    if determine_os() == "nt":
        sock = join_multicast_windows(mcast_grp, mcast_port, ip_addr)
    elif determine_os() == "posix":
        sock = join_multicast_posix(mcast_grp, mcast_port, ip_addr)

    if sock is None:
        print("error getting network interface")
        return
    return sock


def parse_psn_packet(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    psn_id = unpack("<H", buffer[0:2])[0]
    if psn_id in iter(PsnV1Chunk):
        pass  # PSN V1 not supported by this parser
    elif psn_id in iter(PsnV2Chunck):
        chunk_id, chunk_buffer, _ = parse_chunk(buffer)
        if chunk_id == PsnV2Chunck.PSN_INFO_PACKET:
            return parse_info(chunk_buffer)
        elif chunk_id == PsnV2Chunck.PSN_DATA_PACKET:
            return parse_data(chunk_buffer)


def parse_chunk(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    chunk_id, data_field = unpack("<HH", buffer[0:4])
    data_len = data_field & 0x7FFF
    data = buffer[4:4 + data_len]
    rest = None

    if data_len + 8 < len(buffer):
        rest = buffer[data_len + 4:]
    return chunk_id, data, rest


def parse_info(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    info = None
    system_name = None
    trackers = None

    while buffer:
        chunk_id, chunk_buffer, buffer = parse_chunk(buffer)
        if chunk_id == PsnInfoChunk.PSN_INFO_PACKET_HEADER:
            info = parse_header(chunk_buffer[:12])
        elif chunk_id == PsnInfoChunk.PSN_INFO_SYSTEM_NAME:
            system_name = parse_system_name(chunk_buffer)
        elif chunk_id == PsnInfoChunk.PSN_INFO_TRACKER_LIST:
            trackers = parse_info_tracker_list(chunk_buffer)

    if info and system_name and trackers:
        packet = PsnInfoPacket(info, system_name, trackers)
        return packet
    else:
        return None


def parse_data(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    info = None
    trackers = None

    while buffer:
        chunk_id, chunk_buffer, buffer = parse_chunk(buffer)
        if chunk_id == PsnDataChunk.PSN_DATA_PACKET_HEADER:
            info = parse_header(chunk_buffer[:12])
        elif chunk_id == PsnDataChunk.PSN_DATA_TRACKER_LIST:
            trackers = parse_data_tracker_list(chunk_buffer)

    if info and trackers:
        packet = PsnDataPacket(info, trackers)
        return packet
    else:
        return None


def parse_header(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    (
        timestamp,
        version_high,
        version_low,
        frame_id,
        packet_count
    ) = unpack("<QBBBB", buffer)

    info = PsnInfo(
        timestamp,
        version_high,
        version_low,
        frame_id,
        packet_count
    )

    return info


def parse_system_name(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    # TODO: may cause unicode issues?
    system_name = buffer
    return system_name


def parse_info_tracker_list(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    trackers: List["PsnTrackerInfo"] = []
    while buffer:
        tracker_id, chunk_buffer, buffer = parse_chunk(buffer)

        if len(chunk_buffer) > 0:
            while chunk_buffer:
                chunk_id, info_buffer, chunk_buffer = parse_chunk(chunk_buffer)
                if chunk_id == PasnTrackerListChunk.PSN_INFO_TRACKER_NAME:
                    # TODO: encoding issues?
                    tracker_name = info_buffer
                    tracker = PsnTrackerInfo(tracker_id, tracker_name)
                    trackers.append(tracker)
    return trackers


def parse_data_tracker_list(buffer):
    """_summary_

    Args:
        buffer (_type_): _description_

    Returns:
        _type_: _description_
    """
    trackers: List["PsnTracker"] = []
    while buffer:
        tracker_id, chunk_buffer, buffer = parse_chunk(buffer)

        tracker = PsnTracker(tracker_id)

        if len(chunk_buffer) > 0:
            while chunk_buffer:
                chunk_id, data_buffer, chunk_buffer = parse_chunk(chunk_buffer)
                if chunk_id in iter(PsnTrackerChunk):
                    vector = PsnVector3(*unpack("<fff", data_buffer))
                    if chunk_id == PsnTrackerChunk.PSN_DATA_TRACKER_POS:
                        tracker.pos = vector
                    elif chunk_id == PsnTrackerChunk.PSN_DATA_TRACKER_ORI:
                        tracker.ori = vector
                    elif chunk_id == PsnTrackerChunk.PSN_DATA_TRACKER_ACCEL:
                        tracker.accel = vector
                    elif chunk_id == PsnTrackerChunk.PSN_DATA_TRACKER_SPEED:
                        tracker.speed = vector
                    elif (
                        chunk_id ==
                        PsnTrackerChunk.PSN_DATA_TRACKER_TRGTPOS
                    ):
                        tracker.trgtpos = vector

                elif (
                    chunk_id ==
                    PsnTrackerChunkInfo.PSN_DATA_TRACKER_STATUS
                ):
                    status = unpack("<f", data_buffer)[0]
                    tracker.status = status
                elif (
                    chunk_id ==
                    PsnTrackerChunkInfo.PSN_DATA_TRACKER_TIMESTAMP
                ):
                    timestamp = unpack("<L", data_buffer[:4])[0]
                    tracker.timestamp = timestamp
        trackers.append(tracker)
    return trackers


def prepare_psn_info_packet_bytes(
    info_packet: PsnInfoPacket
):
    """_summary_

    Args:
        info_packet (PsnInfoPacket): _description_

    Returns:
        _type_: _description_
    """
    trackers_packet_bytes = b''
    tot_enc_tracker_name_length = 0

    for tracker in info_packet.trackers:
        encoded_tracker_name = str.encode(tracker.tracker_name)
        tracker_name_len = len(encoded_tracker_name)

        tot_enc_tracker_name_length = (
            tot_enc_tracker_name_length
            + tracker_name_len + 16
        )
        trackers_packet_bytes = (
            trackers_packet_bytes
            + pack(
                "<HHHH" + str(tracker_name_len) + "s",
                tracker.tracker_id,
                tracker_name_len + 4,
                PasnTrackerListChunk.PSN_INFO_TRACKER_NAME,
                tracker_name_len,
                encoded_tracker_name,
            )
        )
    trackers_packet_bytes = (
        pack(
            "<HH",
            PsnInfoChunk.PSN_INFO_TRACKER_LIST,
            4 + tot_enc_tracker_name_length + 4
        )
        + trackers_packet_bytes
    )

    encoded_system_name = str.encode(info_packet.name)
    system_name_lenght = len(encoded_system_name)
    info_packet_bytes = (
        pack(
            (
                "<HHHHQBBBBHH"
                + str(system_name_lenght)
                + "s"
            ),
            PsnV2Chunck.PSN_INFO_PACKET,
            (
                20 + system_name_lenght + tot_enc_tracker_name_length
            ),
            PsnInfoChunk.PSN_INFO_PACKET_HEADER,
            12,
            info_packet.info.timestamp,
            info_packet.info.version_high,
            info_packet.info.version_low,
            info_packet.info.frame_id,
            info_packet.info.packet_count,
            PsnInfoChunk.PSN_INFO_SYSTEM_NAME,
            system_name_lenght,
            encoded_system_name
        )
        + trackers_packet_bytes
    )

    return info_packet_bytes


def prepare_psn_data_packet_bytes(
    data_packet: PsnDataPacket
):
    """_summary_

    Args:
        data_packet (PsnDataPacket): _description_

    Returns:
        _type_: _description_
    """
    trackers_packet_bytes = b''
    tot_enc_tracker_length = 0

    for tracker in data_packet.trackers:
        tot_enc_tracker_length = (
            tot_enc_tracker_length
            + 100  # (10 * 4) + (5 * 12)
        )
        trackers_packet_bytes = (
            trackers_packet_bytes
            + pack(
                "<HHHHfffHHfffHHfffHHfffHHfffHHfHHL",
                tracker.id,
                96,  # (9 * 4) + (5 * 12)
                PsnTrackerChunk.PSN_DATA_TRACKER_POS,
                12,
                tracker.pos.x,
                tracker.pos.y,
                tracker.pos.z,
                PsnTrackerChunk.PSN_DATA_TRACKER_ORI,
                12,
                tracker.ori.x,
                tracker.ori.y,
                tracker.ori.z,
                PsnTrackerChunk.PSN_DATA_TRACKER_ACCEL,
                12,
                tracker.accel.x,
                tracker.accel.y,
                tracker.accel.z,
                PsnTrackerChunk.PSN_DATA_TRACKER_SPEED,
                12,
                tracker.speed.x,
                tracker.speed.y,
                tracker.speed.z,
                PsnTrackerChunk.PSN_DATA_TRACKER_TRGTPOS,
                12,
                tracker.trgtpos.x,
                tracker.trgtpos.y,
                tracker.trgtpos.z,
                PsnTrackerChunkInfo.PSN_DATA_TRACKER_STATUS,
                4,
                tracker.status,
                PsnTrackerChunkInfo.PSN_DATA_TRACKER_TIMESTAMP,
                4,
                tracker.timestamp,
            )
        )
    trackers_packet_bytes = (
        pack(
            "<HH",
            PsnDataChunk.PSN_DATA_TRACKER_LIST,
            4 + tot_enc_tracker_length
        )
        + trackers_packet_bytes
    )

    data_packet_bytes = (
        pack(
            (
                "<HHHHQBBBB"
            ),
            PsnV2Chunck.PSN_DATA_PACKET,
            (
                20 + tot_enc_tracker_length
            ),
            PsnDataChunk.PSN_DATA_PACKET_HEADER,
            12,
            data_packet.info.timestamp,
            data_packet.info.version_high,
            data_packet.info.version_low,
            data_packet.info.frame_id,
            data_packet.info.packet_count
        )
        + trackers_packet_bytes
    )

    return data_packet_bytes


def send_psn_packet(
    psn_packet,
    mcast_ip='236.10.10.10',
    ip_addr="0.0.0.0",
    mcast_port=56565
):
    """_summary_

    Args:
        psn_packet (_type_): _description_
        mcast_ip (str, optional): _description_. Default '236.10.10.10'.
        ip_addr (str, optional): _description_. Default "0.0.0.0".
        mcast_port (int, optional): _description_. Default to 56565.
    """
    with multicast_expert.McastTxSocket(
        socket.AF_INET,
        mcast_ips=[mcast_ip],
        iface_ip=ip_addr
    ) as mcast_tx_sock:

        for mcast_ip in mcast_ip:
            mcast_tx_sock.sendto(psn_packet, (mcast_ip, mcast_port))
