import unittest

from tulha.items.items_compilation import \
    ItemsCompilation, loads_from_stream


class SerializableItemsCompilation(unittest.TestCase):
    def test_serialization(self):
        """
        Encodes some compilations of items and decode them back.
        Items in the decoded compilation must match the original.
        """
        compilations = sample_compilations()

        for compilation in compilations:
            serialized_compilaton = compilation.dumps()
            decoded_compilation, errors = loads_from_stream(
                serialized_compilaton)

            assert (errors is None)
            self.assertDictEqual(compilation.entries,
                                 decoded_compilation.entries)

    def test_error_on_deserializing_invalid_stream(self):
        """
        Verify that trying to deserialize invalid streams fails gracefully.
        """
        # Stream without meaningful information
        invalid_stream = [0x80]
        decoded_compilation, message = loads_from_stream(invalid_stream)
        assert (message is not None)
        assert ('error' in message.lower())
        self.assertDictEqual(decoded_compilation.entries, {})

    def test_keeping_decoded_items_on_deserialization_error(self):
        """
        Verify that trying to deserialize partially invalid streams
        fails gracefully.
        """
        # Stream corrupted at last item
        compilation = build_sample_compilationB()
        invalid_stream = compilation.dumps()
        invalid_stream.pop()

        decoded_compilation, message = loads_from_stream(invalid_stream)
        assert (message is not None)
        assert ('error' in message.lower())

        compilation_without_last_item = compilation.entries
        compilation_without_last_item.popitem()
        self.assertDictEqual(decoded_compilation.entries,
                             compilation_without_last_item)


def sample_compilations() -> list[ItemsCompilation]:
    """
    Returns a list of ItemsCompilation for testing purposes.
    """
    return [
        ItemsCompilation(),
        build_sample_compilationA(),
        build_sample_compilationB()
    ]


def build_sample_compilationA() -> ItemsCompilation:
    """
    Returns a compilation of entries with empty fields.
    """
    entries = [
        ('', ''),
        ('', ''),
        ('', ''),
    ]
    return _build_compilation(entries)


def build_sample_compilationB() -> ItemsCompilation:
    """
    Returns a compilation of entries with special characters.
    """
    entries = [
        ('A', '123'),
        ('B', 'This is text B'),
        ('Título 6?', '!\nsome new\ntext@!'),
        ('Secret Verse', 'নমস্কাৰ, মোৰ মৰমৰ বন্ধু।'),
        ('12345679', 'Այս տեքստային դաշտի մասին ոչ ոքի մի պատմիր։'),
        ('Secret Verse', 'هناك طيور في السماء\r\n! الكثير!'),
    ]
    return _build_compilation(entries)


def _build_compilation(title_text_pairs: list[(str, str)]) -> ItemsCompilation:
    compilation = ItemsCompilation()

    for title, text in title_text_pairs:
        compilation.add_entry(title, text)

    return compilation
