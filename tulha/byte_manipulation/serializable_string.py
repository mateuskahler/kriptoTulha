from .serializable_unsigned import dumps as serialize_unsigned
from .serializable_unsigned import loads_from_stream as unserialize_unsigned


def dumps(value: str) -> bytearray:
    """
    input: a Python String

    returns:
        bytearray containing the serialized representation of input
    """
    encoded_utf8 = value.encode(encoding='utf-8')
    encoded_size = len(encoded_utf8)

    output = serialize_unsigned(encoded_size)
    output.extend(encoded_utf8)

    return output


def loads_from_stream(stream: memoryview) -> tuple[str, int]:
    """
    stream: memoryview starting at serialized string position

    returns:
        tuple(value, bytes_consumed)
        value: the string read from the stream
        bytes_consumed: how many byte were required
            (the stream should advance this amount to read the next item)
    """
    expected_string_size, bytes_consumed_so_far = unserialize_unsigned(stream)
    required_bytes = expected_string_size + bytes_consumed_so_far

    if len(stream) < required_bytes:
        raise RuntimeError('End of stream reached')

    raw_utf8 = bytes(stream[bytes_consumed_so_far: required_bytes])

    try:
        value = raw_utf8.decode(encoding='utf-8')
    except UnicodeDecodeError:
        raise ValueError('Invalid utf-8 input')

    return value, required_bytes
