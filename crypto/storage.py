from .keyring import generate_key
from .stamp import generate_integrity_stamp, validate_integrity_stamp
from .crypt import encode_message, decode_message

from .parameters import KEY_DERIVATION_SALT_SIZE, \
    INTEGRITY_STAMP_HASH_SIZE, \
    INTEGRITY_STAMP_SALT_SIZE, \
    ENCRYPT_CHACHA_NONCE_SIZE


def write_to_file(filename: str,
                  content: bytes,
                  user_password: str):
    password = user_password.encode(encoding='utf-8')

    file_content = assemble_encrypted_file(content, password)
    with open(filename, 'wb') as destination_file:
        destination_file.write(file_content)


def load_from_file(filename: str,
                   user_password: str) -> bytes:
    password = user_password.encode(encoding='utf-8')

    with open(filename, 'rb') as source_file:
        content = source_file.read()

    file_valid, recovered_content = disassemble_encrypted_file(
        content, password)

    if file_valid is True:
        return recovered_content
    else:
        raise RuntimeError(
            f'Error interpreting the file {filename}. '
            'Probably wrong password provided.')


def assemble_encrypted_file(content: bytes, password: bytes) -> bytes:
    primary_key, primary_salt = generate_key(password)
    secondary_key, secondary_salt = generate_key(password)

    stamp = generate_integrity_stamp(
        content, secondary_key)
    decoded_content_stamped = secondary_salt + content + stamp

    encoded_message = encode_message(decoded_content_stamped, primary_key)

    return primary_salt + encoded_message


def disassemble_encrypted_file(file_content: bytes,
                               password: bytes) -> tuple[bool, bytes]:
    check_file_size(file_content)

    primary_salt, encoded_message = extract_key_derivation_salt(file_content)
    primary_key, _ = generate_key(password, primary_salt)

    decoded_content_salted_stamped = decode_message(
        encoded_message, primary_key)

    secondary_salt, decoded_content_stamped = extract_key_derivation_salt(
        decoded_content_salted_stamped)
    secondary_key, _ = generate_key(password, secondary_salt)

    decoded_content, stamp = extract_stamp(decoded_content_stamped)

    content_valid = validate_integrity_stamp(
        decoded_content, stamp, secondary_key)

    return (content_valid, decoded_content)


def check_file_size(file_content: bytes):
    minimun_size = (2 * KEY_DERIVATION_SALT_SIZE) + \
        ENCRYPT_CHACHA_NONCE_SIZE + \
        INTEGRITY_STAMP_SALT_SIZE + INTEGRITY_STAMP_HASH_SIZE

    provided_content_size = len(file_content)

    if provided_content_size < minimun_size:
        raise RuntimeError(
            f'File has wrong size. '
            f'Expected at least size {minimun_size} bytes, '
            f'content has size {provided_content_size}.')


def extract_key_derivation_salt(file_content: bytes) -> tuple[bytes, bytes]:
    salt = file_content[:KEY_DERIVATION_SALT_SIZE]
    extracted_content = file_content[KEY_DERIVATION_SALT_SIZE:]

    return (salt, extracted_content)


def extract_stamp(content_stamped: bytes) -> tuple[bytes, bytes]:
    stamp_size = INTEGRITY_STAMP_SALT_SIZE + INTEGRITY_STAMP_HASH_SIZE

    decoded_content = content_stamped[:-stamp_size]
    stamp = content_stamped[-stamp_size:]

    return (decoded_content, stamp)
