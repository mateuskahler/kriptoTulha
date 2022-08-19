import unittest

from itertools import product

from crypto.crypt import encode_message, decode_message
from crypto.salt import generate_salt

from crypto.parameters import ENCRYPT_CHACHA_KEY_SIZE, \
    ENCRYPT_CHACHA_NONCE_SIZE


class ChaChaEncryption(unittest.TestCase):
    def test_decryption(self):
        """
        Encrypt and decrypt some messages.
        The decrypted message must match the original.
        """
        for message in self.messages:
            key = generate_salt(ENCRYPT_CHACHA_KEY_SIZE)

            encrypted = encode_message(message, key)
            decrypted = decode_message(encrypted, key)

            self.assertEqual(message, decrypted)

    def test_wrong_key_size_error(self):
        """
        Trying to encode a message with wrong key size generates expected
        error.
        """
        key_sizes = list(range(1, ENCRYPT_CHACHA_KEY_SIZE * 2))

        for (message, key_size) in product(self.messages, key_sizes):
            if key_size == ENCRYPT_CHACHA_KEY_SIZE:
                continue

            key = generate_salt(key_size)
            self.assertRaisesRegex(RuntimeError, "wrong size",
                                   encode_message,
                                   message, key)

    def test_message_too_small_error(self):
        """
        Trying to decode a message too small to contain a nonce raises the
        expected error
        """
        for message in self.messages:
            key = generate_salt(ENCRYPT_CHACHA_KEY_SIZE)
            encrypted = encode_message(message, key)
            truncated = encrypted[:ENCRYPT_CHACHA_NONCE_SIZE - 1]

            self.assertRaisesRegex(RuntimeError, "too small",
                                   decode_message,
                                   truncated, key)

    def test_encrypt_empty_message(self):
        """
        Encryption and decryption of an empty message works
        """
        for _ in range(10):
            key = generate_salt(ENCRYPT_CHACHA_KEY_SIZE)
            encrypted = encode_message(bytes([]), key)
            decrypted = decode_message(encrypted, key)

            self.assertEqual(bytes([]), decrypted)

    def setUp(self):
        self.messages = [
            'A sample message'.encode(encoding='UTF-8'),
            'Pão com açúcar'.encode(encoding='UTF-8'),
            bytes([0x0d, 0x63, 0x54, 0x32, 0xcf, 0x8a, 0x89, 0x37, 0x70,
                   0x24, 0x1c, 0xfa, 0x69, 0xed, 0xcd, 0xaa, 0x03, 0xf8,
                   0xa0, 0x6e, 0x64, 0x20, 0xf2, 0xa8, 0x7a, 0x29, 0x28,
                   0xcb, 0x59, 0x82, 0x89, 0x42, 0xce, 0x84, 0x45, 0x5e,
                   0x7d, 0x0c, 0x48, 0x2f, 0x66, 0xa1, 0x7a, 0xd0, 0x17,
                   0xc6, 0xb7, 0xf4, 0x15, 0x6e, 0xcc, 0xde, 0x23, 0xef,
                   0xf9, 0xe5, 0xa9, 0xfd, 0xe2, 0x69, 0xf8, 0xac, 0x3f]),
            'A'.encode(encoding='UTF-8'),
            'A message repeated many times!\n'.encode(encoding='UTF-8') * 666,
            bytes([0]),
        ]
        return super().setUp()
