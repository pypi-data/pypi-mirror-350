#!/usr/bin/env python3
import curses
import textwrap
import subprocess
import sys
import os
import shlex
import argparse
import tempfile
import termios


def main(stdscr, header_lines, display_text, interpreter):
    # initialize curses modes and colors
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.clear()

    # get terminal size
    height, width = stdscr.getmaxyx()
    # wrap and draw header lines with 1-col margin
    wrapped_header = []
    for h in header_lines:
        wrapped_header.extend(textwrap.wrap(h, width - 4) or [h])
    header_height = len(wrapped_header)

    # define pager box coordinates with 1-tile margin
    top = header_height + 1
    left = 1
    right = width - 2
    bottom = height - 2  # leave last line for prompt
    # content area inside box
    content_height = bottom - top - 1
    content_width = right - left - 1

    # prepare display lines wrapped to content_width
    lines = []
    for line in display_text.splitlines() or [""]:
        lines.extend(textwrap.wrap(line, content_width) or [""])
    max_offset = max(len(lines) - content_height, 0)
    offset = 0

    options = ["Yes", "No"]
    selection = 1  # default No
    prompt = "Do you want to run this script?"

    while True:
        stdscr.erase()
        # draw header with margin
        for i, hline in enumerate(wrapped_header):
            stdscr.addstr(i + 1, 2, hline)
        # draw box border
        stdscr.addch(top, left, curses.ACS_ULCORNER)
        stdscr.addch(top, right, curses.ACS_URCORNER)
        stdscr.addch(bottom, left, curses.ACS_LLCORNER)
        stdscr.addch(bottom, right, curses.ACS_LRCORNER)
        # horizontal lines
        stdscr.hline(top, left + 1, curses.ACS_HLINE, content_width)
        stdscr.hline(bottom, left + 1, curses.ACS_HLINE, content_width)
        # vertical lines
        for y in range(top + 1, bottom):
            stdscr.addch(y, left, curses.ACS_VLINE)
            stdscr.addch(y, right, curses.ACS_VLINE)
        # display content inside box
        for i in range(content_height):
            idx = offset + i
            if idx < len(lines):
                stdscr.addstr(top + 1 + i, left + 1, lines[idx])
        # draw prompt and options
        stdscr.addstr(height - 1, 1, prompt)
        x = len(prompt) + 3
        for idx, opt in enumerate(options):
            if idx == selection:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(height - 1, x, f" {opt} ")
            if idx == selection:
                stdscr.attroff(curses.A_REVERSE)
            x += len(opt) + 4
        stdscr.refresh()

        key = stdscr.getch()
        if key in (curses.KEY_UP, ord("k")):
            offset = max(0, offset - 1)
        elif key in (curses.KEY_DOWN, ord("j")):
            offset = min(offset + 1, max_offset)
        elif key == curses.KEY_NPAGE:
            offset = min(offset + content_height, max_offset)
        elif key == curses.KEY_PPAGE:
            offset = max(0, offset - content_height)
        elif key in (curses.KEY_LEFT, ord("h")):
            selection = max(0, selection - 1)
        elif key in (curses.KEY_RIGHT, ord("l")):
            selection = min(len(options) - 1, selection + 1)
        elif key in (curses.KEY_ENTER, 10, 13):
            return options[selection]


def run():
    parser = argparse.ArgumentParser(
        description="Preview a script from stdin and confirm before running it."
    )
    parser.add_argument(
        "--header",
        help="Optional header text above the pager",
        default="Script preview:",
    )
    args = parser.parse_args()

    # read script from stdin
    if sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)

    script_text = sys.stdin.read()
    if not script_text.strip():
        print("Error: no script provided on stdin.", file=sys.stderr)
        sys.exit(1)

    # detect shebang or default
    lines = script_text.splitlines()
    if lines and lines[0].startswith("#!"):
        shebang = lines[0][2:].strip()
        interpreter = shlex.split(shebang)
        display_text = script_text
    else:
        interpreter = ["/bin/bash"]
        display_text = "#!/bin/bash\n" + script_text

    header_lines = args.header.splitlines() if args.header else []

    # redirect stdio to tty for curses
    try:
        fd = os.open("/dev/tty", os.O_RDWR)
        os.dup2(fd, 0)
        os.dup2(fd, 1)
        os.dup2(fd, 2)
    except OSError:
        pass

    # launch TUI
    try:
        choice = curses.wrapper(main, header_lines, display_text, interpreter)
    except Exception:
        curses.endwin()
        raise

    # execute or cancel
    if choice == "Yes":
        # write the script to a temp file to allow interactive input
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", prefix="hyscript_", suffix=".sh"
        ) as tf:
            tf.write(script_text)
            tf_path = tf.name
        os.chmod(tf_path, 0o700)
        try:
            subprocess.run("reset")
            subprocess.run(interpreter + [tf_path], check=True)
        finally:
            os.unlink(tf_path)
        sys.exit(0)
    else:
        print("Cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    run()
