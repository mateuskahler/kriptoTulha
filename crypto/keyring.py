import argon2

from .salt import validate_salt


def generate_key(password: bytes, salt: bytes = None) -> tuple[bytes, bytes]:
    """
    Given a password and an optional salt, returns the generated key and the salt.
    If no salt is given, a random one is generated.
    If a wrong length salt is given, a new random one is generated.

    Password must be bytes (or a list thereof). Cannot be a string!

    Calling this function again with same pasword and salt generates the same key.
    """
    from .parameters import KEY_DERIVATION_SALT_SIZE, \
        KEY_DERIVATION_THREADS, KEY_DERIVATION_KEY_SIZE, \
        KEY_DERIVATION_ITERATIONS, KEY_DERIVATION_MEMORY, \
        KEY_DERIVATION_ARGON_TYPE

    salt = validate_salt(salt, KEY_DERIVATION_SALT_SIZE)

    generated_key = argon2.low_level.hash_secret_raw(
        secret=password, salt=salt,
        time_cost=KEY_DERIVATION_ITERATIONS, memory_cost=KEY_DERIVATION_MEMORY,
        parallelism=KEY_DERIVATION_THREADS, hash_len=KEY_DERIVATION_KEY_SIZE,
        type=KEY_DERIVATION_ARGON_TYPE)

    return generated_key, salt
