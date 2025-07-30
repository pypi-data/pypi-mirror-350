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
"""controller
"""

import curses
import threading
import time
from collections import deque

import can
import cantools
from cyber.python.cyber_py3 import cyber
from modules.common_msgs.chassis_msgs import chassis_pb2
from modules.common_msgs.control_msgs import control_cmd_pb2

from akbc import screen


class KeyboardController:

    def __init__(self, scr, dbc_file='./vehicle.dbc', device='can0'):
        self.scr = scr
        self.node = cyber.Node('simple-vehicle-controller')
        self.reader = self.node.create_reader('/apollo/canbus/chassis',
                                              chassis_pb2.Chassis,
                                              self.on_chassis)
        self.writer = self.node.create_writer('/apollo/control',
                                              control_cmd_pb2.ControlCommand)
        self.db = cantools.database.load_file(dbc_file)
        self.canbus = can.Bus(
            interface='socketcan',
            channel=device,
            bitrate=500000,
        )
        self.threads = []
        self.period = 0.1
        self.gear_location_idx = 0
        self.motion_mode_idx = 0

        self.controls = {
            'driving_mode': 0,
            'steering_target': 0.0,
            'steering_rate': 0.0,
            'acceleration': 0.0,
            'gear_location': 0,
            'motion_mode': 1,
        }
        self.chassis = {
            'engine_started': 0.0,
            'speed_mps': 0,
            'gear_location': 0,
            'driving_mode': 0,
            'motion_mode': 0,
            'stickcontrol_event': 0,
            'steering_angle': 0.0,
            'steering_angle_speed': 0.0,
            'longitudinal_acceleration': 0.0,
        }

        self.logs = deque(maxlen=20)
        self.control_cmd_msg = control_cmd_pb2.ControlCommand()

        # register keyboard handlers
        self.scr.on(ord('q'), self.handle_input)
        self.scr.on(curses.KEY_UP, self.handle_input)
        self.scr.on(curses.KEY_DOWN, self.handle_input)
        self.scr.on(curses.KEY_LEFT, self.handle_input)
        self.scr.on(curses.KEY_RIGHT, self.handle_input)
        self.scr.on(ord('m'), self.handle_input)
        self.scr.on(ord('s'), self.handle_input)
        self.scr.on(ord('g'), self.handle_input)

        self._stop_event = threading.Event()

    def log(self, message):
        """log
        """
        self.logs.append(f'{time.strftime("%H:%M:%S")} - {message}')

    def draw_vehicle(self):
        """draw vehicle
        """
        self.scr.vehicle_win.draw_raw([
            r'   _____',
            u'  /_____\\',
            r'  |o   o|',
            r'  |     |',
            r'  |     |',
            r'  |o   o|',
            u'  |-----|',
        ], 2, 2)

    def draw_controls(self):
        """draw controls
        """
        self.scr.controls_win.draw('Controls:', [
            'Up/Down: Acceleration/Brake',
            'Left/Right: Turn Left/Right',
            's: Switch autodriving mode',
            'm: Switch motion mode',
            'g: Switch gear location',
            'Q: Quit',
        ])

    def draw_status(self):
        """draw chassis status
        """
        self.scr.status_win.draw('Chassis:', [
            f'engine_started: {self.chassis["engine_started"]}',
            f'gear_location: {self.chassis["gear_location"]}',
            f'driving_mode: {self.chassis["driving_mode"]}',
            f'steering_angle: {self.chassis["steering_angle"]} deg',
            (r'steering_angle_speed: '
             f'{self.chassis["steering_angle_speed"]} deg/s'),
            f'speed_mps: {self.chassis["speed_mps"]} m/s',
            (r'longitudinal_acceleration: '
             f'{self.chassis["longitudinal_acceleration"]} m/s^2'),
            f'stickcontrol_event: {self.chassis["stickcontrol_event"]}',
            f'motion_mode: {self.chassis["motion_mode"]}',
        ], curses.A_BOLD | curses.color_pair(1))

    def draw_logs(self):
        """draw operation logs
        """
        content = []
        for log in self.logs:
            content.append(log[:self.scr.log_win.width - 4])

        self.scr.log_win.draw('Logs:', content,
                              curses.A_BOLD | curses.color_pair(2))

    def on_update_screen(self):
        """on_update_screen
        """
        self.draw_vehicle()
        self.draw_controls()
        self.draw_status()
        self.draw_logs()

    def handle_input(self, key):
        """handle_input
        """
        if key == curses.KEY_UP:
            if self.controls['acceleration'] >= 0:
                self.controls['acceleration'] += 0.1
            else:
                self.controls['acceleration'] = 0
            self.log(f'accelerated to {self.controls["acceleration"]} m/s^2')

        elif key == curses.KEY_DOWN:
            if self.controls['acceleration'] <= 0:
                self.controls['acceleration'] -= 0.1
            else:
                self.controls['acceleration'] = 0
            self.log(f'braked to {self.controls["acceleration"]} m/s^2')

        elif key == curses.KEY_LEFT:
            if self.controls['motion_mode'] == 2:
                self.controls['steering_rate'] += 0.5
                self.log(
                    f'steering_rate: {self.controls["steering_rate"]} deg/s')
            else:
                self.controls['steering_target'] += 0.5
                self.log(
                    f'steering_target: {self.controls["steering_target"]} deg')

        elif key == curses.KEY_RIGHT:
            if self.controls['motion_mode'] == 2:
                self.controls['steering_rate'] -= 0.5
                self.log(
                    f'steering_rate: {self.controls["steering_rate"]} deg/s')
            else:
                self.controls['steering_target'] -= 0.5
                self.log(
                    f'steering_target: {self.controls["steering_target"]} deg')

        elif key == ord('m'):
            # switch motion mode
            motions = [1, 2, 3, 4, 5]
            self.motion_mode_idx = (self.motion_mode_idx + 1) % len(motions)
            self.controls['motion_mode'] = motions[self.motion_mode_idx]
            self.log(f'set motion_mode to {self.controls["motion_mode"]}.')

        elif key == ord('s'):
            # switch autodriving mode
            if self.controls['driving_mode'] == 0:
                self.controls['driving_mode'] = 1
            else:
                self.controls['driving_mode'] = 0
            self.log(f'driving_mode to {self.controls["driving_mode"]}.')

        elif key == ord('g'):
            # switch gear location
            gears = [0, 1, 2, 3]
            self.gear_location_idx = (self.gear_location_idx + 1) % len(gears)
            self.controls['gear_location'] = gears[self.gear_location_idx]
            self.log(f'set gear_location to {self.controls["gear_location"]}.')

    def on_chassis(self, chassis):
        """on_chassis
        """
        # TODO(All): select fields via config
        self.chassis['engine_started'] = chassis.engine_started
        self.chassis['speed_mps'] = chassis.speed_mps
        self.chassis['gear_location'] = chassis.gear_location
        self.chassis['driving_mode'] = chassis.driving_mode
        self.chassis['motion_mode'] = chassis.motion_mode
        self.chassis['stickcontrol_event'] = chassis.stickcontrol_event
        self.chassis['steering_angle'] = chassis.steering_angle
        self.chassis['steering_angle_speed'] = chassis.steering_angle_speed
        self.chassis[
            'longitudinal_acceleration'] = chassis.longitudinal_acceleration

    def get_control_command(self):
        """get_control_command
        """
        self.control_cmd_msg.Clear()
        self.control_cmd_msg.pad_msg.driving_mode = self.controls[
            'driving_mode']
        if self.controls['driving_mode'] == 1:
            self.control_cmd_msg.pad_msg.action = 1
        else:
            self.control_cmd_msg.pad_msg.action = 0
        self.control_cmd_msg.motion_mode = self.controls['motion_mode']
        self.control_cmd_msg.gear_location = self.controls['gear_location']
        self.control_cmd_msg.acceleration = self.controls['acceleration']
        self.control_cmd_msg.steering_target = self.controls['steering_target']
        self.control_cmd_msg.steering_rate = self.controls['steering_rate']
        return self.control_cmd_msg

    def on_update(self):
        """on_update
        """
        while self.running():
            cmd = self.get_control_command()
            self.writer.write(cmd)

            self.on_update_screen()
            time.sleep(self.period)

    def running(self):
        """running
        """
        return not self._stop_event.is_set()

    def run(self):
        self.log("System started")

        update_thread = threading.Thread(target=self.on_update)
        self.threads.append(update_thread)
        update_thread.start()

        update_thread.join()

    def shutdown(self):
        """shutdown
        """
        self._stop_event.set()


def main(stdscr):
    """main entry
    """
    cyber.init()

    curses.use_default_colors()

    scr = screen.Screen(stdscr)
    controller = KeyboardController(scr)

    threading.Thread(target=scr.run).start()

    try:
        controller.run()
    except KeyboardInterrupt:
        controller.shutdown()
        controller.log("System interrupted by user")
    finally:
        controller.shutdown()
        cyber.shutdown()


if __name__ == '__main__':
    curses.wrapper(main)
