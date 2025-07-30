#!/usr/bin/env python
"""apollo keyboard controller
"""
import curses
import signal
import threading
import traceback

import click
from cyber.python.cyber_py3 import cyber

from akbc import canbus_monitor, keyboard_controller, screen, simple_vehicle


@click.command()
@click.option('--disable_keyboard_controller', is_flag=True, default=False)
@click.option('--enable_virtual_vehicle', is_flag=True, default=False)
@click.option('--dbc_file', default='./vehicle.dbc', type=str, help='dbc file')
@click.option('--device', default='can0', type=str, help='can device')
@click.option(
    '--initial_x',
    # default=587362.114900,
    default=586389.25,
    type=float,
    help='initial x')
@click.option(
    '--initial_y',
    # default=4140841.386400,
    default=4140674.01,
    type=float,
    help='initial y')
@click.option(
    '--initial_yaw',
    # default=-0.614823,
    default=2.891656162,
    type=float,
    help='initial yaw')
@click.option(
    '--wheelbase',
    default=0.96,
    type=float,
    help='vehicle wheelbase, default 0.96, unit: m',
)
@click.option(
    '--vin',
    default='12345678901234567',
    type=str,
    help='vehicle vin, default 12345678901234567',
)
def main(**kwargs):
    """main entry
    """
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    scr = screen.Screen(stdscr)

    cyber.init()

    controller = None
    if not kwargs['disable_keyboard_controller']:
        controller = keyboard_controller.KeyboardController(
            scr, kwargs['dbc_file'], kwargs['device'])
    vehicle = None
    if kwargs['enable_virtual_vehicle']:
        vehicle = simple_vehicle.SimpleVehicle(
            scr, kwargs['dbc_file'], kwargs['device'], kwargs['initial_x'],
            kwargs['initial_y'], kwargs['initial_yaw'], kwargs['vin'],
            kwargs['wheelbase'])
    monitor = canbus_monitor.CanbusMonitor(kwargs['dbc_file'],
                                           kwargs['device'])

    def _show_canbus_data():
        """_show_canbus_data
        """
        content = monitor.get_showing_text()
        scr.canbus_win.draw('Canbus:', content,
                            curses.A_BOLD | curses.color_pair(1))

    scr.ontick(_show_canbus_data)

    def _vehicle_pause_handler(_):
        """_vehicle_pause_handler
        """
        if vehicle:
            if vehicle.paused:
                vehicle.resume()
            else:
                vehicle.pause()

    def _vehicle_reset_handler(_):
        """_vehicle_reset_handler
        """
        if vehicle:
            vehicle.reset()

    if vehicle:
        scr.on(ord(' '), _vehicle_pause_handler)
        scr.on(ord('r'), _vehicle_reset_handler)

    threads = []
    screen_thread = threading.Thread(target=scr.run, name='screen')
    threads.append(screen_thread)
    monitor_thread = threading.Thread(target=monitor.run, name='monitor')
    threads.append(monitor_thread)
    if controller:
        controller_thread = threading.Thread(target=controller.run,
                                             name='controller')
        threads.append(controller_thread)
    if vehicle:
        vehicle_thread = threading.Thread(target=vehicle.run, name='vehicle')
        threads.append(vehicle_thread)

    def _exit_screen(_):
        """_exit_curses
        """
        if controller:
            controller.shutdown()
        if vehicle:
            vehicle.shutdown()
        cyber.shutdown()
        monitor.shutdown()
        scr.shutdown()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    scr.on(ord('q'), _exit_screen)

    def _signal_handler(sig, frame):
        """signal_handler
        """
        print('exiting...', sig)
        exit_signals = [signal.SIGINT, signal.SIGTERM]
        if sig in exit_signals:
            if controller:
                controller.shutdown()
            if vehicle:
                vehicle.shutdown()
            cyber.shutdown()
            monitor.shutdown()
            scr.shutdown()
            stdscr.keypad(False)
            curses.echo()
            curses.endwin()
        else:
            # unhandled signal
            print(f'Unhandled signal: {sig}', traceback.print_stack(frame))

    # register signal handlers
    signal.signal(signal.SIGINT, _signal_handler)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    # screen_thread.join()


if __name__ == '__main__':
    main()
