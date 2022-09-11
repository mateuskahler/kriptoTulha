from tulha import ItemsCompilation, loads_from_stream
from crypto import load_from_file, write_to_file
from user_interface import KryptoTulhaUserInterface


def main():
    open_main_window()


def load_file(path: str, user_password: str) \
        -> tuple[ItemsCompilation | None, str | None]:
    content = load_from_file(path, user_password)
    return loads_from_stream(content)


def save_file(compilation: ItemsCompilation, path: str, user_password: str) \
        -> None:
    content = compilation.dumps()
    write_to_file(path, content, user_password)


def open_main_window():
    app = KryptoTulhaUserInterface(save_file, load_file)
    app.assume_control()


if __name__ == "__main__":
    main()
