from Cryptodome.Cipher import ChaCha20
from .salt import generate_salt

from .parameters import ENCRYPT_CHACHA_NONCE_SIZE, ENCRYPT_CHACHA_KEY_SIZE


def encode_message(message: memoryview, key: bytes) -> bytes:
    check_key_size(key)

    nonce = generate_salt(ENCRYPT_CHACHA_NONCE_SIZE)
    cipher = ChaCha20.new(key=key, nonce=nonce)
    crypt_message = cipher.encrypt(message)

    return crypt_message + nonce


def decode_message(encoded_message: memoryview, key: bytes) -> bytes:
    check_key_size(key)

    (encoded_message, nonce) = split_encoded_and_nonce(encoded_message)
    cipher = ChaCha20.new(key=key, nonce=nonce)

    return cipher.decrypt(encoded_message)


def split_encoded_and_nonce(encoded_message: bytes) -> tuple[bytes, bytes]:
    provided_message_size = len(encoded_message)

    if provided_message_size < ENCRYPT_CHACHA_NONCE_SIZE:
        raise RuntimeError(
            f'Encoded message too small to contain nonce. '
            f'Expected size >= {ENCRYPT_CHACHA_NONCE_SIZE}, '
            f'received {provided_message_size}.')

    crypt_message = encoded_message[:-ENCRYPT_CHACHA_NONCE_SIZE]
    nonce = encoded_message[-ENCRYPT_CHACHA_NONCE_SIZE:]

    return (crypt_message, nonce)


def check_key_size(key: bytes):
    provided_key_size = len(key)

    if provided_key_size != ENCRYPT_CHACHA_KEY_SIZE:
        raise RuntimeError(
            f'Encryption key has wrong size. '
            f'Expected {ENCRYPT_CHACHA_KEY_SIZE}, '
            f'received {provided_key_size}.')
