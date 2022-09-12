import unittest

from itertools import product

from tulha.items.items_compilation import \
    ItemsCompilation, loads_from_stream

from crypto.storage import write_to_file, load_from_file
from crypto.salt import generate_salt

TEST_FILE_NAME = 'testing.kryptoTulha'


class SaveLoadFiles(unittest.TestCase):
    def test_save_and_load_ItemsCompilation_to_file(self):
        """
        Serialize some items, encrypt them using predefined passwords and save
        to a file. The file is then opened and decrypted back using the same
        password. The process must succeed in recovering the original items.
        """
        for user_password, compilation in \
                product(self.passwords, self.compilations):
            compilation_as_bytes = compilation.dumps()
            write_to_file(TEST_FILE_NAME, compilation_as_bytes, user_password)

            recovered_bytes = load_from_file(TEST_FILE_NAME, user_password)
            recovered_compilation, errors = loads_from_stream(recovered_bytes)

            assert (errors is None)

            self.assertDictEqual(
                recovered_compilation.entries, compilation.entries)

    def setUp(self):
        self.passwords = [
            "SampleP4ssword",
            "A",
            "スーパーシークレット",
            "0123456789"
        ]

        items_count = [0, 1, 5, 20, 100]
        self.compilations = [sample_compilation(i) for i in items_count]

        return super().setUp()


def sample_compilation(items_count: int) -> ItemsCompilation:
    """
    Returns a ItemsCompilation for testing purposes.
    """
    compilation = ItemsCompilation()
    for i in range(items_count):
        compilation.add_entry(*generate_item(i))

    return compilation


def generate_item(item_id: int) -> tuple[str, str]:
    """
    Generates a pair of (title, content) for testing pourposes.
    """
    if item_id == 1:
        title = "How Do I Love Thee"
        text = """How do I love thee? Let me count the ways.
I love thee to the depth and breadth and height
My soul can reach, when feeling out of sight
For the ends of being and ideal grace.
I love thee to the level of every day's
Most quiet need, by sun and candle-light.
I love thee freely, as men strive for right.
I love thee purely, as they turn from praise.
I love thee with the passion put to use
In my old griefs, and with my childhood's faith.
I love thee with a love I seemed to lose
With my lost saints. I love thee with the breath,
Smiles, tears, of all my life; and, if God choose,
I shall but love thee better after death.

-- Elizabeth Barrett Browning"""

    elif item_id == 2:
        title = "Bank Romenia"
        text = """password one: h()ASDy9aIHD8SD)A09Q@3y
password two: çmsdfp8u02n1sz-9134"""

    elif item_id == 3:
        title = "Flip Table Emoji"
        text = """(╯°□°)╯  ┻━┻
┬─┬ノ(ಠ_ಠノ)

( °□°) ︵ ┻━┻

 ~ ┻━┻ ~ ¯\\(◡ ‿ ◡¯\\)

ʕノ•ᴥ•ʔノ ︵ ┻━┻

"""
    elif item_id == 4:
        title = 'Title and no Text'
        text = ''

    elif item_id == 5:
        title = ''
        text = 'Text and no Title'

    elif item_id == 6:
        title = ''
        text = ''

    else:
        title = "Sample Title "
        title += f"{int(generate_salt(1)[0])} {int(generate_salt(1)[0])}"
        text = f"Some random bytes:\n{str(generate_salt(10))}"

    return (title, text)
