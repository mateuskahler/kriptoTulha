from user_interface import KryptoTulhaUserInterface


def main():
    open_main_window()


def open_main_window():
    app = KryptoTulhaUserInterface([], None, None)
    app.assume_control()


if __name__ == "__main__":
    main()
