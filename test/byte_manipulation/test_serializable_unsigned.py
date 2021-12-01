import unittest
from tulha.byte_manipulation.serializable_unsigned import \
    dumps, loads_from_stream


class SerializableUnsigned(unittest.TestCase):
    def test_serialization(self):
        """
        Encodes some numbers and decode them back.
        The decoded value must match the original value.
        """
        numbers = range(99999)

        for number in numbers:
            serialized = dumps(number)
            number_read, _ = loads_from_stream(serialized)

            self.assertEqual(number, number_read)

    def test_serialization_large_number(self):
        """
        Encodes some large numbers and decode them back.
        The decoded value must match the original value.
        """
        numbers = [
            123456789123456789,
            10101010101010101010101010,
            3241654646371646354163,
            666666666666666666666666666666,
            0xFFFFFFFFFFFFFFFFFF,
            0xc0a0c0cacaca00caca00c73c1
        ]

        for number in numbers:
            serialized = dumps(number)
            number_read, _ = loads_from_stream(serialized)

            self.assertEqual(number, number_read)

    def test_bytes_consumed(self):
        """
        Encodes some numbers, insert the result on a bytestream and verifies
        that, when decoding, the amount of bytes consumed is the same as the
        bytes required to encode the numbers.
        """
        numbers = [
            0,
            1,
            2,
            67,
            1548,
            1569879,
            987653166,
            16468789796641,
            416479868463164676843135210,
        ]
        for number in numbers:
            serialized = list(dumps(number))
            bytes_generated = len(serialized)

            fake_stream = bytes([1, 2, 3, 4] + serialized + [1, 2, 3, 4])

            _, bytes_consumed = loads_from_stream(fake_stream[4:])

            self.assertEqual(bytes_consumed, bytes_generated)

    def test_error_on_serializing_negative_numbers(self):
        """
        Verify that trying to serialize negative numbers raises
        the correct exception.
        """
        self.assertRaises(ValueError, dumps, -1)
        self.assertRaises(ValueError, dumps, -77)
        self.assertRaises(ValueError, dumps, -666)

    def test_error_on_deserializing_invalid_stream(self):
        """
        Verify that trying to deserialize an invalid stream raises
        the correct exception.
        """
        invalid_stream = [0x80]
        self.assertRaisesRegex(RuntimeError, "End of stream",
                               loads_from_stream, invalid_stream)

        invalid_stream = [234, 193, 185, 129, 233,
                          202, 135, 225, 232, 149, 132, 196]
        self.assertRaisesRegex(RuntimeError, "End of stream",
                               loads_from_stream, invalid_stream)
