import unittest
from tulha.byte_manipulation.serializable_string import \
    dumps, loads_from_stream


class SerializableString(unittest.TestCase):
    def test_serialization(self):
        """
        Encodes some strings and decode them back.
        The decoded value must match the original value.
        """
        strings_examples = [
            'This is just ASCII. 123!?',
            '如果不是全部，自由又是多少？',
            'A 📐🐘 🐶 🔂 🗣️ 👤⬅️ 👤👨🏼 has nothing much 💬',
            'O verso é repetido 1000 vezes (...) ' * 1000
        ]

        for string_sample in strings_examples:
            serialized = dumps(string_sample)
            string_read, _ = loads_from_stream(serialized)

            self.assertEqual(string_sample, string_read)

    def test_bytes_consumed(self):
        """
        Encodes some strings, insert the result on a bytestream and verifies
        that, when decoding, the amount of bytes consumed is the same as the
        bytes required to encode the strings.
        """
        strings_examples = [
            'This is just ASCII. 123!?',
            '如果不是全部，自由又是多少？',
            'A 📐🐘 🐶 🔂 🗣️ 👤⬅️ 👤👨🏼 has nothing much 💬',
            'O verso é repetido 1000 vezes (...) ' * 1000
        ]

        for string_sample in strings_examples:
            serialized = list(dumps(string_sample))
            bytes_generated = len(serialized)

            fake_stream = bytes([1, 2, 3, 4] + serialized + [1, 2, 3, 4])

            _, bytes_consumed = loads_from_stream(fake_stream[4:])

            self.assertEqual(bytes_consumed, bytes_generated)

    def test_error_on_deserializing_short_stream(self):
        """
        Verify that trying to deserialize an incomplete stream raises
        the correct exception.
        """
        invalid_stream = [0x80]
        self.assertRaisesRegex(RuntimeError, "End of stream",
                               loads_from_stream, invalid_stream)

        invalid_stream = [234, 193, 185, 129, 233,
                          202, 135, 225, 232, 149, 132, 196]
        self.assertRaisesRegex(RuntimeError, "End of stream",
                               loads_from_stream, invalid_stream)

    def test_error_on_deserializing_short_stream(self):
        """
        Verify that trying to deserialize invalid utf-8 raises the 
        correct exception.
        """
        # (Not sure I will ever handle this, but still)
        invalid_sequences = [
            b"\xc3\x28",
            b"\xa0\xa1",
            b"\xe2\x28\xa1",
            b"\xe2\x82\x28",
            b"\xf0\x28\x8c\xbc",
            b"\xf0\x90\x28\xbc",
            b"\xf0\x28\x8c\x28",
            b"\xf8\xa1\xa1\xa1\xa1",
            b"\xfc\xa1\xa1\xa1\xa1\xa1",
        ]

        from tulha.byte_manipulation.serializable_unsigned import \
            dumps as serialize_unsigned

        for invalid_sequence in invalid_sequences:
            # We have to manually create the stream, since the encoding in invalid
            invalid_stream = serialize_unsigned(len(invalid_sequence))
            invalid_stream.extend(invalid_sequence)

            self.assertRaisesRegex(ValueError, "Invalid utf-8",
                                   loads_from_stream, invalid_stream)
