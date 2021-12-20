from secrets import token_bytes


def generate_salt(nbytes):
    return token_bytes(nbytes)
