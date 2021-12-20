import argon2

from .salt import generate_salt


def generate_key(password, salt: bytes = None) -> tuple[bytes, bytes]:
    from .parameters import KEY_DERIVATION_SALT_SIZE, \
        KEY_DERIVATION_THREADS, KEY_DERIVATION_KEY_SIZE, \
        KEY_DERIVATION_ITERATIONS, KEY_DERIVATION_MEMORY, \
        KEY_DERIVATION_ARGON_TYPE

    if salt is None:
        salt = generate_salt(KEY_DERIVATION_SALT_SIZE)

    generated_key = argon2.low_level.hash_secret_raw(
        password, salt,
        KEY_DERIVATION_ITERATIONS, KEY_DERIVATION_MEMORY,
        KEY_DERIVATION_THREADS, KEY_DERIVATION_KEY_SIZE,
        KEY_DERIVATION_ARGON_TYPE)

    return generated_key, salt
