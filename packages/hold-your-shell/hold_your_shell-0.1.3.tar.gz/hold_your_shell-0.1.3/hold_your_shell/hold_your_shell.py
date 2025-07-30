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

TABS = ["Script Preview", "Env Vars"]


def main(stdscr, display_text, env_vars_text, interpreter):
    curses.curs_set(0)
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    curses.start_color()
    if curses.can_change_color():
        curses.init_color(curses.COLOR_BLACK, 0, 0, 0)
    curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
    stdscr.bkgd(" ", curses.color_pair(1))

    height, width = stdscr.getmaxyx()
    top = 2
    left = 1
    right = width - 2
    bottom = height - 2
    content_height = bottom - top - 1
    content_width = right - left - 1

    tab_index = 0
    offset = 0
    options = ["Yes", "No"]
    selection = 1
    prompt = "Do you want to run this script?"

    def get_lines():
        text = display_text if tab_index == 0 else env_vars_text
        lines = []
        for line in text.splitlines() or [""]:
            lines.extend(textwrap.wrap(line, content_width) or [""])
        return lines

    lines = get_lines()
    max_offset = max(len(lines) - content_height, 0)

    while True:
        stdscr.erase()

        # draw tabs
        x = 2
        for i, tab in enumerate(TABS):
            if i == tab_index:
                stdscr.attron(curses.A_REVERSE)
            stdscr.addstr(1, x, f" {tab} ")
            if i == tab_index:
                stdscr.attroff(curses.A_REVERSE)
            x += len(tab) + 3
        # stdscr.addstr(1, x, "(press TAB)")

        # draw box
        stdscr.addch(top, left, curses.ACS_ULCORNER)
        stdscr.addch(top, right, curses.ACS_URCORNER)
        stdscr.addch(bottom, left, curses.ACS_LLCORNER)
        stdscr.addch(bottom, right, curses.ACS_LRCORNER)
        stdscr.hline(top, left + 1, curses.ACS_HLINE, content_width)
        stdscr.hline(bottom, left + 1, curses.ACS_HLINE, content_width)
        for y in range(top + 1, bottom):
            stdscr.addch(y, left, curses.ACS_VLINE)
            stdscr.addch(y, right, curses.ACS_VLINE)

        # display content
        lines = get_lines()
        max_offset = max(len(lines) - content_height, 0)
        for i in range(content_height):
            idx = offset + i
            if idx < len(lines):
                stdscr.addstr(top + 1 + i, left + 1, lines[idx])

        # prompt
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
        elif key == 9:  # Tab
            tab_index = (tab_index + 1) % len(TABS)
            offset = 0
        elif key in (curses.KEY_ENTER, 10, 13):
            return options[selection]
        elif key in (27, ord("q")):
            return "No"


def run():
    parser = argparse.ArgumentParser(
        description="Preview a script from stdin and confirm before running it."
    )
    args = parser.parse_args()

    if sys.stdin.isatty():
        parser.print_help(sys.stderr)
        sys.exit(1)

    script_text = sys.stdin.read()
    if not script_text.strip():
        print("Error: no script provided on stdin.", file=sys.stderr)
        sys.exit(1)

    lines = script_text.splitlines()
    if lines and lines[0].startswith("#!"):
        shebang = lines[0][2:].strip()
        interpreter = shlex.split(shebang)
        display_text = script_text
    else:
        interpreter = [os.getenv("SHELL", "/bin/bash")]
        display_text = f"#!{interpreter[0]}\n" + script_text

    env_vars_text = "\n".join(f"{k}={v}" for k, v in os.environ.items())

    try:
        fd = os.open("/dev/tty", os.O_RDWR)
        os.dup2(fd, 0)
        os.dup2(fd, 1)
        os.dup2(fd, 2)
    except OSError:
        pass

    try:
        choice = curses.wrapper(main, display_text, env_vars_text, interpreter)
    except Exception:
        curses.endwin()
        raise

    if choice == "Yes":
        with tempfile.NamedTemporaryFile(
            delete=False, mode="w", prefix="hyscript_", suffix=".sh"
        ) as tf:
            tf.write(script_text)
            tf_path = tf.name
        os.chmod(tf_path, 0o700)
        try:
            subprocess.run("reset")
            subprocess.run(interpreter + [tf_path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error: exit code {e.returncode}", file=sys.stderr)
            sys.exit(1)
        finally:
            os.unlink(tf_path)
        sys.exit(0)
    else:
        print("Cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    run()
