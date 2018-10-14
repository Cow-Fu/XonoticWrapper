import curses
from curses import textpad

class ThreadManager:
    def __init__(self):
        pass

class Curser:

    def __init__(self, x, y, maxX, maxY):
        self.x = x
        self.y = y


def inputWinInit(win):
    pass

def outputWinInit(win):
    pass

def loop(stdscr):
    pass
    # main loop

def init(stdscr):
    # Initialization
    # stdscr.clear()
    # curses.echo()
    height, width = stdscr.getmaxyx()
    title = "Xonotic Wrapper (Ctrl+c to exit)"
    stdscr.addstr(0, (width // 2)-(len(title) // 2), title)
    # stdscr.keypad(True)

def main(stdscr):
    stdscr.immedok(True)
    init(stdscr)
    stdscr.refresh()

    height, width = stdscr.getmaxyx()

    # height, width, begin_y, begin_x
    winInput = curses.newwin(3, width - 2, height - 3, 2)
    winOutput = curses.newwin(height - 4, width - 2, 1, 2)

    winInput.immedok(True)
    winOutput.immedok(True)


    winInput.box()
    winInput = textpad.Textbox(winInput, insert_mode=True)
    winOutput.box()
    # winInput.addstr()
    winOutput.addstr(1, 1, "Hello World!")
    # winInput.refresh()
    winOutput.refresh()
    winInput.edit()
    # winInput.getch()
    stdscr.getch()

if __name__ == '__main__':
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        curses.nocbreak()
        curses.echo()
        curses.endwin()
        print("Exiting!")
# import curses
# import textwrap
#
# screen = curses.initscr()
# screen.immedok(True)
# try:
#     screen.border(0)
#
#     box1 = curses.newwin(20, 40, 6, 50)
#     box2 = curses.newwin(18,38,7,51)
#     box1.immedok(True)
#     box2.immedok(True)
#     text = "I want all of this text to stay inside its box. Why does it keep going outside its borders?"
#     text = "The quick brown fox jumped over the lazy dog."
#     text = "A long time ago, in a galaxy far, far away, there lived a young man named Luke Skywalker."
#     box1.box()
#     box2.addstr(1, 0, textwrap.fill(text, 38))
#
#     #box1.addstr("Hello World of Curses!")
#
#     screen.getch()
#
# finally:
#     curses.endwin()
