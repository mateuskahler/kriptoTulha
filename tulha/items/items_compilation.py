from .single_item import SingleItem


class ItemsCompilation:
    def __init__(self):
        self.entries: dict[int, SingleItem] = {}
        self.id_counter = 0

    def add_entry(self, title: str, text: str) -> int:
        new_id = self._generate_new_id()
        self.entries[new_id] = SingleItem(title, text)

        return new_id

    def dumps(self) -> bytearray:
        """
        returns:
            bytearray containing the serialized representation of this instance
        """
        from .single_item import dumps as dumps_entry
        output = bytearray()

        for item in self.entries.values():
            output.extend(dumps_entry(item))

        return output

    def existing_ids(self) -> list[int]:
        return list(self.entries.keys())

    def get_item_by_id(self, iid: int) -> SingleItem:
        return self.entries[iid]

    def change_text_of_item_by_id(self, iid: int, new_text: str):
        current_item = self.entries[iid]
        new_item = SingleItem(title=current_item.title, text=new_text)
        self.entries[iid] = new_item

    def _generate_new_id(self) -> int:
        self.id_counter += 1
        return self.id_counter


def loads_from_stream(stream: memoryview) \
        -> tuple[ItemsCompilation, str | None]:
    """
    Tries to decode a stream into a ItemsCompilation.
    In case of any errors, it keeps the succesfully decoded items
    and returns a message signaling the error.

    input:
        stream: memoryview starting at serialized ItemsCompilation position

    returns:
        tuple(value, message)
        value: the ItemsCompilation read from the stream
        message: a message signaling success or any error
    """
    output = ItemsCompilation()
    stream_position = 0
    error = None

    from .single_item import loads_from_stream as load_item
    while stream_position < len(stream):
        try:
            new_item, bytes_consumed = load_item(stream[stream_position:])
            output.add_entry(new_item.title, new_item.text)
            stream_position += bytes_consumed

        except Exception as e:
            error = e
            break

    if error is not None:
        return (output,
                f'Error loading data! {len(output.entries)} items recoverd. '
                f'Error: {error}')
    else:
        return (output, None)
