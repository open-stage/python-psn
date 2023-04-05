import binascii
from pathlib import Path


def test_parsing(pypsn_module):
    """Initial test example method"""

    test_data_file_path = Path(Path(__file__).parents[0], "data.log")

    with open(test_data_file_path) as psn_data:
        for psn_line in psn_data.readlines():
            psn_line = psn_line.strip().replace("b'", "").replace("'", "")
            hexdata = binascii.unhexlify(psn_line)
            data = pypsn_module.parse_psn_packet(hexdata)
            test_vector = pypsn_module.psn_vector3(
                -15.247539520263672, 6.0, -60.15142822265625
            )
            if isinstance(data, pypsn_module.psn_data_packet):
                print(data.trackers[0].pos)
                assert test_vector == data.trackers[0].pos
            # TODO: improve me - add psn_info_packet test
