import curses
import time

if __name__ == "__main__":
    # try:
    stdscr = curses.initscr()
    curses.noecho()

    for t in range(0, 10):
        stdscr.clear()
        stdscr.addstr("a"*11400+str(t))
        stdscr.refresh()
        time.sleep(1)
    # except:
    #     # Exception by Ctrl + C
    #     pass
    # finally:
    #     curses.echo()
    #     curses.endwin()