#!/usr/bin/env python
# Copyright 2025 Pride Leong <lykling.lyk@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""screen
"""

import curses
import time


class Screen:
    """Screen
    """

    class Window:
        """Window
        """

        def __init__(self, stdscr, height, width, y, x):
            """__init__
            """
            self.stdscr = stdscr
            self.height = height
            self.width = width
            self.y = y
            self.x = x

            self.win = curses.newwin(height, width, y, x)
            self.win.keypad(True)
            self.win.scrollok(True)
            self.win.idlok(True)
            self.win.idcok(True)
            self.win.box()
            self.win.noutrefresh()

        def draw_raw(self, lines, padding_x=0, padding_y=0):
            """draw_raw
            """
            self.win.erase()
            for i, line in enumerate(lines):
                self.win.addstr(i + padding_y, padding_x, line)
            self.win.box()
            self.win.noutrefresh()

        def draw(self, title, lines, title_style=curses.A_BOLD):
            """draw
            """
            self.win.erase()
            self.win.addstr(1, 2, title, title_style)
            for i, line in enumerate(lines):
                self.win.addstr(i + 3, 2, line)
            self.win.box()
            self.win.noutrefresh()

    def __init__(self, stdscr):
        """__init__
        """
        self.stdscr = stdscr

        # init colors
        curses.start_color()
        curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)

        curses.use_default_colors()

        # layout
        #
        # |---------------------------|
        # |         |          |      |
        # | vehicle | controls | logs |
        # |         |          |      |
        # | ------------------ |      |
        # |         |          |      |
        # | chassis | status   |      |
        # |         |          |      |
        # |---------------------------|
        # |                           |
        # |   canbus signals          |
        # |                           |
        # |---------------------------|
        height, width = self.stdscr.getmaxyx()
        vehicle_win_coords = (11, int(width * 0.3), 0, 0)
        self.vehicle_win = self.Window(self.stdscr, *vehicle_win_coords)
        controls_win_coords = (11, int(width * 0.3), 0, int(width * 0.3) + 1)
        self.controls_win = self.Window(self.stdscr, *controls_win_coords)

        status_win_coords = (16, int(width * 0.3), 11, 0)
        self.status_win = self.Window(self.stdscr, *status_win_coords)
        world_win_coords = (16, int(width * 0.3), 11, int(width * 0.3) + 1)
        self.world_win = self.Window(self.stdscr, *world_win_coords)

        canbus_win_coords = (height - 27, width, 27, 0)
        self.canbus_win = self.Window(self.stdscr, *canbus_win_coords)
        log_win_coords = (27, width - int(width * 0.6), 0,
                          int(width * 0.6) + 1)
        self.log_win = self.Window(self.stdscr, *log_win_coords)

        self.listeners = {}
        self.tick_callbacks = []
        self.running = False

    def refresh(self):
        """refresh
        """
        if self.running:
            curses.doupdate()

    def on(self, key, callback):
        """on
        """
        self.listeners[key] = callback

    def off(self, key):
        """off
        """
        if key in self.listeners:
            del self.listeners[key]

    def ontick(self, callback):
        """ontick
        register callback invoked every tick
        """
        self.tick_callbacks.append(callback)

    def offtick(self, callback):
        """offtick
        unregister callback invoked every tick
        """
        self.tick_callbacks.remove(callback)

    def run(self):
        """run
        """
        self.running = True
        curses.curs_set(0)
        self.stdscr.nodelay(True)
        self.stdscr.clear()
        self.stdscr.refresh()

        while self.running:
            try:
                key = self.stdscr.getch()
                if key in self.listeners:
                    self.listeners[key](key)

                self.refresh()
            except curses.error:
                # no input
                pass
            for cb in self.tick_callbacks:
                try:
                    cb()
                except Exception:
                    continue

            time.sleep(0.01)

    def shutdown(self):
        """shutdown
        """
        self.running = False
        self.listeners.clear()
        self.tick_callbacks.clear()
        self.stdscr.clear()
        self.stdscr.refresh()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
