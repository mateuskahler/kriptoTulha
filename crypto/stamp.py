from hashlib import blake2b
from hmac import compare_digest
from .salt import validate_salt


def generate_integrity_stamp(message: memoryview, crypo_key: bytes) -> bytes:
    calculated_hash, salt = generate_hash(message, crypo_key)

    return bytes(calculated_hash + salt)


def validate_integrity_stamp(message: memoryview, stamp: bytes,
                             crypo_key: bytes) -> bool:
    from .parameters import INTEGRITY_STAMP_HASH_SIZE, \
        INTEGRITY_STAMP_SALT_SIZE

    expected_stamp_size = INTEGRITY_STAMP_HASH_SIZE + INTEGRITY_STAMP_SALT_SIZE
    provided_stamp_size = len(stamp)
    if provided_stamp_size != expected_stamp_size:
        raise RuntimeError(
            f'Integrity stamp has wrong size. '
            f'Expected {expected_stamp_size}, '
            f'received {provided_stamp_size}.')

    provided_hash = stamp[:INTEGRITY_STAMP_HASH_SIZE]
    salt = stamp[INTEGRITY_STAMP_HASH_SIZE:]
    calculated_hash, _ = generate_hash(message, crypo_key, salt)

    return compare_digest(calculated_hash, provided_hash)


def generate_hash(message: memoryview, crypo_key: bytes,
                  salt: bytes = None) -> tuple[bytes, bytes]:
    from .parameters import INTEGRITY_STAMP_HASH_SIZE, \
        INTEGRITY_STAMP_SALT_SIZE

    salt = validate_salt(salt, INTEGRITY_STAMP_SALT_SIZE)

    hasher = blake2b(
        message,
        digest_size=INTEGRITY_STAMP_HASH_SIZE,
        key=crypo_key,
        salt=salt)

    return hasher.digest(), salt
