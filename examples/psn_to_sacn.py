#! /bin/env python
# MIT License
#
# Copyright (C) 2023 Matthew Franklin, vanous
#
# This file is part of pypsn.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
Simple forwarder of PSN to DMX. Turns all coordinates to positive ints.
Requires sacn module: pip install sacn
"""

import sacn
import pypsn


sender = sacn.sACNsender()


def start_dmx():
    """
    Start DMX sender thread.
    """
    sender.start()  # start the sending thread
    sender.activate_output(1)  # start sending out data in the 1st universe
    sender[1].multicast = True  # set multicast to True


def stop_dmx():
    """
    Stop DMX sender thread.
    """
    sender.stop()  # do not forget to stop the sender


def start_psn():
    """
    Start PSN receiver thread.
    """
    pypsn.Receiver(fill_dmx, "192.168.20.177").start()


def fill_dmx(psn_data):
    """
        Callback when PSN dat received.
        Gets the PSN coordinates and tranfers them to DMX.

    Args:
        psn_data (psnDataPacket): psn data class
    """
    if isinstance(psn_data, pypsn.PsnDataPacket):
        position = psn_data.trackers[0].pos
        dmx_data = [0] * 512
        dmx_data[0] = int(abs(position.x))
        dmx_data[1] = int(abs(position.y))
        dmx_data[2] = int(abs(position.z))

        sender[1].dmx_data = dmx_data


if __name__ == "__main__":
    start_dmx()
    start_psn()
