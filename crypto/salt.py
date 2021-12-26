from secrets import token_bytes


def generate_salt(nbytes):
    return token_bytes(nbytes)


def validate_salt(salt, required_size) -> bytes:
    """
    Validate given salt: should be convertible to required_size bytes.

    If the provided salt is valid, return it.
    If it's not, returns a new random valid one.
    """
    if salt is None:
        salt = generate_salt(required_size)

    try:
        salt = bytes(salt)
    except TypeError:
        salt = generate_salt(required_size)

    if len(salt) != required_size:
        salt = generate_salt(required_size)

    return salt
