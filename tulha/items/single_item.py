from typing import NamedTuple


SingleItem = NamedTuple("SingleItem", [("title", str), ("text", str)])


def dumps(entry: SingleItem) -> bytearray:
    """
    input: a SingleItem

    returns:
        bytearray containing the serialized representation of input
    """
    from tulha.byte_manipulation import serialize_string
    output = bytearray()

    output.extend(serialize_string(entry.title))
    output.extend(serialize_string(entry.text))

    return output


def loads_from_stream(stream: memoryview) -> tuple[SingleItem, int]:
    """
    stream: memoryview starting at serialized SingleItem position

    returns:
        tuple(value, bytes_consumed)
        value: the SingleItem read from the stream
        bytes_consumed: how many byte were required
            (the stream should advance this amount to read the next item)
    """
    from tulha.byte_manipulation import load_string_from_stream

    title, bytes_consumed_title = load_string_from_stream(stream)
    text, bytes_consumed_text = load_string_from_stream(
        stream[bytes_consumed_title:])

    bytes_consumed = bytes_consumed_title + bytes_consumed_text
    read_dict_entry = SingleItem(title, text)

    return read_dict_entry, bytes_consumed
