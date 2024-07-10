import unicurses as curses
from unicurses import CCHAR


class Application:
    """This class holds the entire state of the application"""


class CursesWindow:
    """This class represent a single curses window"""

    def __init__(self, ysize: int, xsize: int, y: int, x: int):
        self._window = curses.newwin(ysize, xsize, y, x)
        self.panel_pointer = None
        self.lines = ysize
        self.cols = xsize

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

    def to_panel(self):
        """Returns the panel pointer for this window"""
        if not self.panel_pointer:
            self.panel_pointer = curses.new_panel(self._window)

        return self.panel_pointer


class TextBox:
    def __init__(self, displaysize: int, y: int, x: int):
        """Where displaysize is maximum number of characters that will be displayed at a single time"""
        xsize = displaysize + 4
        ysize = 3  # Keeping things efficient
        self.window = CursesWindow(ysize, xsize, y, x)
        self.input_buffer = ""
        self.cursor_idx = 0

    def getch(self) -> int:
        return self.window.getch()

    def to_panel(self):
        return self.window.to_panel()


def curses_settings() -> None:
    """This method runs all the standard curses commands"""
    curses.noecho()
    curses.cbreak()
    curses.curs_set(2)


def draw_help(keys: list[str]) -> None:
    help_line = ", ".join(keys)
    curses.mvaddstr(1, 2, help_line)


if __name__ == "__main__":
    stdscr = curses.initscr()
    curses.wborder(stdscr)

    curses_settings()
    draw_help(["q | Q: quit", "ENTER: select"])

    LINES, COLS = curses.getyx(stdscr)

    curses.refresh()

    window = CursesWindow(10, 30, int((24 - 10) / 2), int((80 - 30) / 2))
    text_box = TextBox(30, int((24 - 10) / 2), int((80 - 30) / 2))

    panels = list()
    panels.append(window.to_panel())
    panels.append(text_box.to_panel())

    current_top = panels[-1]

    for i in range(0, len(panels)):
        next_ptr = 0 if i == (len(panels) - 1) else i + 1
        curses.set_panel_userptr(panels[i], panels[next_ptr])

    while (ch := curses.getch()) is not CCHAR("q") and ch is not CCHAR("Q"):
        if ch == 10:
            window.mvaddstr(2, 2, "Pressed Enter")
            window.refresh()
        elif ch == 9:
            current_top = curses.panel_userptr(current_top)
            curses.top_panel(current_top)
        curses.mvaddstr(2, 2, f"Pressed {chr(ch)}")

        curses.update_panels()
        curses.doupdate()
    curses.endwin()
    exit()
