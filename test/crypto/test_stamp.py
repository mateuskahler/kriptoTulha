import unittest

from crypto.stamp import \
    generate_integrity_stamp, validate_integrity_stamp


class IntegrityStamp(unittest.TestCase):
    def setUp(self):
        self.messages = [
            'This is a test message with known validity stamp!'.encode(
                encoding='UTF-8'),
            'Another sample message including a koala: ʕ •ᴥ•ʔ'.encode(
                encoding='UTF-8'),
            b'\xad\xf3:\xe0.\x82\x9a\xb3\x9d\xef^Y\xb9B\xfd\x8b\xe7\xf4\xca\xb7\x0e'
            b'\xde\x92\x8f\xdc4\xff\xc7\xc7+\xd9\xdd',
        ]

        self.keys = [
            b'\xc6\x9d\x11^ot|\x0co\x12\x05\x9a*\x1b\xd8\xc2\xf9,\x86\xbafYR\xbbN\x80\x9f"\x9d\x07ZF',
            b'XP\xcb9\xce\xcf)*|\xed2`\xa3g\xdcC9\xff\x16_"/\x13\x07 \\\xd0g/\xf4{{',
            b'\xd7\xb1g\xc9_\xcb!QNu\xfd\xce\x15C\x80\xd1\xcf\xad\x8ck\xbd\xd8l\xc0\xe5^\xe2Z\x9e\x11\x80J',
        ]

        # list of valid stamps for each message in self.messages, using each key in self.keys, ordered as in
        # stamp[message_index][key_index]
        self.stamps = [
            [b".\xe1&j};\xb7\x9f|3\x06\x8d\xb5r\x01!\x9b\xa0\xb6\xea\xd7\xc2\xadVFe{\x7f\xb5\xbc\xa1\x96\x94l\x8f\xde"
             b"\x1b\xdcJ'\xbe\x1cJ\xfb\xdc\xa8\x10\xd0g\xc1]\xf6o\x9e\x96\xf53\xff\xf7\xeb\x85\x95<\x8f\xe0\xc0$k\x0c;"
             b"\x82\xfb\x0f\xd1\x01M\xcfIx\xec",
             b'\x81\xbd\xd8\xf3\x8a>\xa5\xd2\\\xb1\x98\xa4\x1e\xa7yMF\x00\x82\xc6+)\x17}\x82\xe3\xfbWw\xff\xfa\xa1\x1b'
             b'\xb3X5\xf0\xbd\xfb\xfe\x96J\x87X\xe0\xe7\xc3\x80Mg\xbc\xee\xa8\x15\xe5\xf85%\xe3 \xa4\x80\x07\x16=\x10'
             b'\xa2j\xe5\xcb:\x91\xa7V\xab\x91\xc0\x92v\x01',
             b'\x8bK\x1c\\\xbe:=\x18\x83]\xe9\x88\x11\t8\x13\xb7\xfcB\xaa\xc1\xd2\x90\xec`\xc5\x1fo-\xe4\xab\xd7\xa3'
             b'\xf9~.eP\xb5\xa9i\x19\x98\xef\xe8\xca7\xf8\x0e\x8f\xb3\n{\x81\xbb\xacf\xca5\xc1@*=\x98\xe8\xc2\xbd\x16'
             b'\x88G~0|aj\x9c0\x9fQ '
             ],
            [b'\xec \x13!\xfd\xb0\x16\xd3\xff\xff\xda\xbc\xd2)\xa2h8\xf1\xed\xd9\xe3\xb4C\x84\xe4\xc9\xd2\xa9\x8aI7\x08'
             b'\x10\x1e1\xff\xf2-\xaf\xe5\x1a\xe3\xae!\xca4\xfa\xa5\xbe\x9eW\x00\xc6\x18K\x179\xfa\xc1}\x89\xf7\xc6'
             b'\x85R\xc0\xd6\xbaW\xfe\xfa,\x97\\\xbedv>AU',
             b'\xf6\xadt\xd2\xfc\x1b\x98\'\xdb\x19"W\xcb\xc0\x821\r\xfd5Z\x93]/\x10\xe0\x97\x16\x86\xbe\x082\x0fJ\xa2bT'
             b'\xcb\xc3\x13Y\x00\x98R\xef\xeb\xd2\x87?\xb4\x12W\x05\xbb\x90+\xc4\x8f\xf7\xa2\x18\xea\xa5\x1e\xa1<\xfa'
             b'\xde\x9eUML#S`\xf80j~\x82\xff',
             b'\xdc?_a\x8d\xa7lP\x8d\xea\xdc8\x05\x01;\xdf\xf8\xe70$\xb5\xa1\xd6\x9c\xf7b\x0f\x8a \x82\x1c\xfaM\xe8t'
             b'\xac:R\xa6FYF\x8b!\xc4\xb6\xb1,Z\x9bf\xb1g\x03\xb7\xe6\x04\x99+M9\x9c\x07\xf9\xcb\xfcvD9\x19U\xf8\x10'
             b'\xb4\xec\xae[6=l'
             ],
            [b'r?\xf1\x06R\x11\x0f\x06\x9e\xc3+\x88\x1b)\xb1[\xea\xe1\xf6\xa1\xba\xb2\xfe\x17\xd3D\x96\x170w\xf3\x1f'
             b'\x89\x93\x8e)\x9cT\xd0\xa8\xd4\x83J,\x0b\x08\x86\xd1\xa1y[\xdfo\xd1W\xe0\xc9<\x06O\x12$\x1d7\xda{\xf8'
             b'\xb6\xd6\xf0\x91\xab2\x05\x83\xbb>\x82\xe6\xda',
             b'\x8b\x1d\x95r\x92\xd0*>\xde\xcc\x10U;\xc4\x15;\x97\xa4\x0bVX\x89\x8e\x01lO\xf4`S09\xd0\xd6nt\x02R\xc5'
             b'\xc9<\xbf\r\x92\x8c\x02l?\x93%Ga\x0fY\x89\xb3\xf3\xf3\x1dy\x05\xacWb\xec\xbc,\xfc\x85!a\xda\xb7w7\xf4k'
             b'\xe38\xad\x1f',
             b"\xf4\xb9\x97z\xe5\xa3\x88\x06%\xbc\x8f\x1d\x87\xa4\xee\x85\x8a+`4#\xdd\xc8\x80\xcb\xa6\x039\xf9\xae\xe7"
             b"\xd9\x11^\x9e\x1c\x8fC(\x8e\xa5y'\x8cq\xd2tM\xf9\x0f\xab\x0c-\xd6\x1e\x91\xca\xc8\x9c\x9e\x81\xd6\xdem"
             b"\x1b\xc0\xd1\xfe\xbdA\xe8\xbd\x87\xa9C\tE\x96\xbdK"
             ]]

        return super().setUp()

    def test_stamp_generation(self):
        """
        Verifies that new integrity stamps - generated using the predefined messages and keys - are evaluated as valid
        stamps.
        """
        for msg_value in self.messages:
            for key_value in self.keys:
                stamp = generate_integrity_stamp(msg_value, key_value)

                self.assertTrue(validate_integrity_stamp(
                    msg_value, stamp, key_value))

    def test_precalculated_stamp_validation(self):
        """
        Verifies that predefined integrity stamps - generated using the predefined messages and keys - are evaluated as
        valid stamps.
        """

        for msg_index, msg_value in enumerate(self.messages):
            for key_index, key_value in enumerate(self.keys):
                calculated_stamp = self.stamps[msg_index][key_index]

                self.assertTrue(validate_integrity_stamp(
                    msg_value, calculated_stamp, key_value))

    def test_stamp_refutal(self):
        """
        Checks if inverting a single bit in predefined integrity stamps - generated using the predefined messages and
        keys - causes corrupted keys to evaluate as invalid.
        """

        for msg_index, msg_value in enumerate(self.messages):
            for key_index, key_value in enumerate(self.keys):
                expected_stamp = self.stamps[msg_index][key_index]
                corrupted_stamp = IntegrityStamp.corrupt_stamp(expected_stamp)

                self.assertFalse(validate_integrity_stamp(
                    msg_value, corrupted_stamp, key_value))

    def corrupt_stamp(stamp: bytes) -> bytes:
        new_stamp = bytearray(stamp)
        new_stamp[0] ^= 1

        return bytes(new_stamp)
