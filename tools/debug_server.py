import unicurses as curses
from unicurses import CCHAR, KEY_ENTER


class Application:
    """This class holds the entire state of the application"""


class CursesWindow:
    """This class represent a single curses window"""

    def __init__(self, ysize: int, xsize: int, y: int, x: int):
        self._window = curses.newwin(ysize, xsize, y, x)

        curses.box(self._window)
        curses.wrefresh(self._window)

    def refresh(self):
        """Updates the terminal with the drawn characters"""
        curses.wrefresh(self._window)

    def mvaddstr(self, y: int, x: int, cstr: str):
        """Write a string at the cursor location"""
        curses.mvwaddstr(self._window, y, x, cstr)

    def getch(self) -> int:
        return curses.wgetch(self._window)


def main():
    global stdscr
    stdscr = curses.initscr()

    curses_settings()
    draw_help(["q | Q: quit", "ENTER: select"])

    curses.refresh()
    window = CursesWindow(10, 30, int((24 - 10) / 2), int((80 - 30) / 2))

    while (ch := curses.getch()) is not CCHAR("q") and ch is not CCHAR("Q"):
        if ch == 10:
            window.mvaddstr(2, 2, "Pressed Enter")
            window.refresh()
        curses.mvaddstr(2, 0, f"Pressed {chr(ch)}")
        curses.addstr(f"ENTER is {KEY_ENTER}")
        curses.clrtoeol()

        curses.doupdate()
    curses.endwin()
    exit()


def curses_settings() -> None:
    """This method runs all the standard curses commands"""
    curses.noecho()
    curses.cbreak()
    curses.curs_set(0)


def draw_help(keys: list[str]) -> None:
    help_line = ", ".join(keys)
    curses.mvaddstr(0, 0, help_line)


if __name__ == "__main__":
    main()
