def dumps(value: int) -> bytearray:
    """
    input: an unsigned integer

    returns:
        bytearray containing the serialized representation of input
    """
    if value < 0:
        raise ValueError('Signed number provided')

    output = bytearray()

    while value > 0x7f:
        output.append((value & 0x7f) | 0x80)
        value >>= 7

    output.append(value)
    return output


def loads_from_stream(stream: memoryview) -> tuple[int, int]:
    """
    stream: memoryview starting at serialized unsigned position

    returns:
        tuple(value, bytes_consumed)
        value: the value read from the stream
        bytes_consumed: how many byte were required
            (the stream should advance this amount to read the next item)
    """
    value = 0
    bytes_consumed = 0
    finished = False

    while (not finished) and (bytes_consumed < len(stream)):
        piece = stream[bytes_consumed]
        value |= (int(piece & 0x7f) << (7*bytes_consumed))
        if (piece & 0x80) == 0:
            finished = True
        bytes_consumed += 1

    if not finished:
        raise RuntimeError('End of stream reached')

    return value, bytes_consumed
