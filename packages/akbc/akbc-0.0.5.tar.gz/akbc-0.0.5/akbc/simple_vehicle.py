#!/usr/bin/env python
"""simple vechile
"""
import curses
import math
import signal
import threading
import time
import traceback

import can
import cantools
import cantools.database
import cantools.database.can.database
import numpy as np
from cyber.python.cyber_py3 import cyber
from modules.common_msgs.localization_msgs import localization_pb2
from scipy.spatial.transform import Rotation

from akbc import screen

exit_event = threading.Event()


def clamp(value, min_value, max_value):
    """clamp
    """
    if value < min_value:
        return min_value
    elif value > max_value:
        return max_value
    else:
        return value


class SimpleVehicle:

    class Attrs:
        """Attrs
        """

        def __init__(self, vin='12345678901234567', wheelbase=0.96):
            """__init__
            """
            self.vin = vin
            self.L = wheelbase

    class State:
        """State
        """

        def __init__(self,
                     initial_x=0.0,
                     initial_y=0.0,
                     initial_yaw=0.0,
                     wheelbase=0.96,
                     vin='12345678901234567'):
            """__init__
            """
            self.auto_driving = 0
            self.takeover = 0
            # pose
            self.x = initial_x
            self.y = initial_y
            self.z = 0.0
            # attitude
            self.pitch = 0.0
            self.roll = 0.0
            self.yaw = initial_yaw

            # displacement
            self.s = 0.0

            # velocity in vehicle axis
            self.velocity_x = 0.0
            self.velocity_y = 0.0
            self.velocity_z = 0.0
            # acceleration in vehicle axis
            self.acceleration_x = 0.0
            self.acceleration_y = 0.0
            self.acceleration_z = 0.0

            # angular velocity
            self.angular_rate_pitch = 0.0
            self.angular_rate_roll = 0.0
            self.angular_rate_yaw = 0.0

            # steering
            self.steering = 0.0
            self.steering_rate = 0.0

            # motion
            self.motion_mode = 1

            # gear
            self.gear = 0

            # error state
            self.errno = 0

    class Messages:
        """Messages
        """

        def __init__(self, database):
            """__init__
            """
            self.db = database

    def __init__(
        self,
        scr,
        dbc_file,
        device,
        initial_x=0.0,
        initial_y=0.0,
        initial_yaw=0.0,
        vin='12345678901234567',
        wheelbase=0.96,
    ):
        """__init__
        """
        self._init_args = {
            'dbc_file': dbc_file,
            'device': device,
            'initial_x': initial_x,
            'initial_y': initial_y,
            'initial_yaw': initial_yaw,
            'vin': vin,
            'wheelbase': wheelbase,
        }
        self.scr = scr
        self.db = cantools.database.load_file(dbc_file)
        if not isinstance(self.db, cantools.database.can.database.Database):
            raise TypeError('dbc_file should be a can database file')

        self.can_bus = can.Bus(
            interface='socketcan',
            channel=device,
            bitrate=500000,
        )

        self.attrs = self.Attrs(vin, wheelbase)
        self.state = self.State(initial_x, initial_y, initial_yaw)

        self.control_messages = [
            self.db.get_message_by_name('ADAS_Heartbeat_Command'),
            self.db.get_message_by_name('ADAS_Vehicle_Mode_Command'),
            self.db.get_message_by_name('ADAS_Vehicle_Drive_Command'),
            self.db.get_message_by_name('IMU_Info'),
        ]
        self.report_messages = [
            self.db.get_message_by_name('VCU_Vehicle_Mode_Report'),
            self.db.get_message_by_name('VCU_Vehicle_Drive_Report'),
            self.db.get_message_by_name('VCU_Error_Report'),
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_01'),
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_02'),
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_03'),
            self.db.get_message_by_name('StickControl'),
        ]
        self.report_messages_last_send_time = {
            self.db.get_message_by_name('VCU_Vehicle_Mode_Report'): 0.0,
            self.db.get_message_by_name('VCU_Vehicle_Drive_Report'): 0.0,
            self.db.get_message_by_name('VCU_Error_Report'): 0.0,
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_01'): 0.0,
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_02'): 0.0,
            self.db.get_message_by_name('VCU_Vehicle_VIN_Report_03'): 0.0,
            self.db.get_message_by_name('StickControl'): 0.0,
        }

        self.bind_report_messages()

        self.node = cyber.Node('simple-vehicle')
        self.pose_writer = self.node.create_writer(
            '/apollo/localization/pose', localization_pb2.LocalizationEstimate)

        self.paused = False
        self._stop_event = threading.Event()

    def bind_report_messages(self):
        """bind_report_messages
        """
        self.report_getters = {}
        # VCU_Vehicle_Drive_Report
        vcu_vehicle_mode_report = self.db.get_message_by_name(
            'VCU_Vehicle_Mode_Report')
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'AutoDriving_STATE')] = lambda: self.state.auto_driving
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'DrivingMode')] = lambda: self.state.motion_mode
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'Gear')] = lambda: self.state.gear
        # VCU_Vehicle_Drive_Report
        vcu_vehicle_mode_report = self.db.get_message_by_name(
            'VCU_Vehicle_Drive_Report')
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'SteerAngle')] = lambda: self.state.steering
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'VehicleAngleSpeed')] = lambda: math.degrees(self.state.
                                                         angular_rate_yaw)
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'LongitudinalAcceleration')] = lambda: self.state.acceleration_x
        self.report_getters[vcu_vehicle_mode_report.get_signal_by_name(
            'VehicleSpeed')] = lambda: math.fabs(self.state.velocity_x)
        # VCU_Error_Report
        vcu_error_report = self.db.get_message_by_name('VCU_Error_Report')
        self.report_getters[vcu_error_report.get_signal_by_name(
            'ErrorCode')] = lambda: self.state.errno
        # VCU_Vehicle_VIN_Report_01
        vcu_vehicle_vin_report_01 = self.db.get_message_by_name(
            'VCU_Vehicle_VIN_Report_01')
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN00')] = lambda: ord(self.attrs.vin[0])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN01')] = lambda: ord(self.attrs.vin[1])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN02')] = lambda: ord(self.attrs.vin[2])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN03')] = lambda: ord(self.attrs.vin[3])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN04')] = lambda: ord(self.attrs.vin[4])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN05')] = lambda: ord(self.attrs.vin[5])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN06')] = lambda: ord(self.attrs.vin[6])
        self.report_getters[vcu_vehicle_vin_report_01.get_signal_by_name(
            'VIN07')] = lambda: ord(self.attrs.vin[7])
        # VCU_Vehicle_VIN_Report_02
        vcu_vehicle_vin_report_02 = self.db.get_message_by_name(
            'VCU_Vehicle_VIN_Report_02')
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN08')] = lambda: ord(self.attrs.vin[8])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN09')] = lambda: ord(self.attrs.vin[9])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN10')] = lambda: ord(self.attrs.vin[10])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN11')] = lambda: ord(self.attrs.vin[11])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN12')] = lambda: ord(self.attrs.vin[12])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN13')] = lambda: ord(self.attrs.vin[13])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN14')] = lambda: ord(self.attrs.vin[14])
        self.report_getters[vcu_vehicle_vin_report_02.get_signal_by_name(
            'VIN15')] = lambda: ord(self.attrs.vin[15])
        # VCU_Vehicle_VIN_Report_03
        vcu_vehicle_vin_report_03 = self.db.get_message_by_name(
            'VCU_Vehicle_VIN_Report_03')
        self.report_getters[vcu_vehicle_vin_report_03.get_signal_by_name(
            'VIN16')] = lambda: ord(self.attrs.vin[16])
        # StickControl
        stickcontrol = self.db.get_message_by_name('StickControl')
        self.report_getters[stickcontrol.get_signal_by_name(
            'TakeOver_CTRL')] = lambda: self.state.takeover

    def on_report(self):
        """on_report
        """
        while self.running():
            # now in millisecond
            now = time.time() * 1000
            for message in self.report_messages:
                if message.cycle_time is None:
                    # not periodic message
                    continue
                if now - self.report_messages_last_send_time[message] < float(
                        message.cycle_time):
                    continue
                data = {}
                for sig in message.signals:
                    if sig in self.report_getters:
                        value = self.report_getters[sig]()
                        if value is not None:
                            data[sig.name] = value
                buffer = message.encode(data)
                msg = can.Message(arbitration_id=message.frame_id,
                                  data=buffer,
                                  is_extended_id=False)
                self.can_bus.send(msg)
                self.report_messages_last_send_time[message] = now
            time.sleep(0.001)

    def on_control_auto_driving(self, auto_driving):
        """on_control_auto_driving
        """
        if auto_driving == self.state.auto_driving:
            return
        self.state.auto_driving = auto_driving
        if auto_driving == 0:
            self.state.velocity_x = 0.0
            self.state.acceleration_x = 0.0
            self.state.steering = 0.0
            self.state.steering_rate = 0.0

    def on_control_motion_mode(self, motion_mode):
        """on_control_motion_mode
        """
        if motion_mode == self.state.motion_mode:
            return
        self.state.motion_mode = motion_mode
        self.state.velocity_x = 0.0
        self.state.acceleration_x = 0.0
        self.state.steering = 0.0
        self.state.steering_rate = 0.0

    def on_control_gear(self, gear):
        """on_control_gear
        """
        if gear == self.state.gear:
            return
        self.state.gear = gear
        self.state.velocity_x = 0.0
        self.state.acceleration_x = 0.0
        self.state.steering = 0.0
        self.state.steering_rate = 0.0

    def on_control_acceleration(self, acceleration, deceleration):
        """on_control_acceleration
        """
        if deceleration > 0:
            self.state.acceleration_x = -deceleration
        else:
            self.state.acceleration_x = acceleration

        self.state.acceleration_x = clamp(self.state.acceleration_x, -10.23,
                                          10.24)

    def on_control_steering(self, steering):
        """on_control_steering
        """
        if self.state.motion_mode == 2:
            return
        self.state.steering = clamp(steering, -163.83, 163.84)

    def on_control_steering_rate(self, steering_rate):
        """on_control_steering_rate
        """
        if self.state.motion_mode != 2:
            return
        self.state.steering_rate = clamp(steering_rate, -327.68, 327.67)
        r = self.attrs.L / 2.0
        self.state.velocity_x = self.state.steering_rate * math.pi / 180 * r

    def on_control(self):
        """on_control
        """
        while self.running():
            message = self.can_bus.recv(timeout=1)
            if message is None:
                continue
            # print('recv message: ', hex(message.arbitration_id),
            #       message.data.hex())
            if message.arbitration_id == self.db.get_message_by_name(
                    'ADAS_Heartbeat_Command').frame_id:
                pass
            elif message.arbitration_id == self.db.get_message_by_name(
                    'ADAS_Vehicle_Mode_Command').frame_id:
                data = self.db.get_message_by_name(
                    'ADAS_Vehicle_Mode_Command').decode(message.data)
                # AutoDriving_CTRL
                self.on_control_auto_driving(data['AutoDriving_CTRL'].value)
                # DrivingMode
                self.on_control_motion_mode(data['DrivingMode_Target'].value)
                # Gear
                self.on_control_gear(data['Gear_Target'].value)
            elif message.arbitration_id == self.db.get_message_by_name(
                    'ADAS_Vehicle_Drive_Command').frame_id:
                data = self.db.get_message_by_name(
                    'ADAS_Vehicle_Drive_Command').decode(message.data)
                # SteerAngle
                self.on_control_steering(data['SteerAngle_Target'])
                # VehicleAngleSpeed
                self.on_control_steering_rate(data['VehicleAngleSpeed_Target'])
                self.on_control_acceleration(
                    data['LongitudinalAcceleration_Target'],
                    data['LongitudinalDeceleration_Target'])
            elif message.arbitration_id == self.db.get_message_by_name(
                    'IMU_Info').frame_id:
                pass
            # time.sleep(0.1)

    def on_update_ackermann(self, dt):
        """on_update_ackermann
        """
        pass
        v = math.fabs(self.state.velocity_x)
        v = clamp(v + self.state.acceleration_x * dt, 0.0, 20.47)
        if self.state.gear == 2:
            self.state.velocity_x = -v
        else:
            self.state.velocity_x = v
        if v < 1e-3:
            v = 0
            return

        heading = self.state.yaw
        steering = self.state.steering
        wheelbase = self.attrs.L

        tan_delta = math.tan(steering * math.pi / 180)
        omega = 0.0
        if math.fabs(tan_delta) > 1e-6:
            omega = v * tan_delta / wheelbase
            if self.state.motion_mode == 5:
                omega = omega * 2.0
            omega = clamp(omega, -327.68 * math.pi / 180,
                          327.67 * math.pi / 180)
        heading = math.fmod(heading + omega * dt, 2 * math.pi)
        ds = math.fabs(self.state.velocity_x) * dt
        dx = ds * math.cos((self.state.yaw + heading) / 2)
        dy = ds * math.sin((self.state.yaw + heading) / 2)
        self.state.x += dx
        self.state.y += dy
        self.state.s += ds
        self.state.yaw = heading
        self.state.angular_rate_yaw = omega

    def on_update_spot_turn(self, dt):
        """on_update_spot_turn
        """
        angular_delta = self.state.steering_rate * dt * math.pi / 180
        self.state.angular_rate_yaw = clamp(angular_delta / dt,
                                            -327.68 * math.pi / 180,
                                            327.67 * math.pi / 180)
        self.state.velocity_x = self.state.angular_rate_yaw * self.attrs.L / 2
        v = math.fabs(self.state.velocity_x)
        if v < 1e-3:
            v = 0
            self.angular_rate_yaw = 0
            return

        direction = 1.0
        if self.state.gear == 4:
            direction = 1.0
        else:
            direction = -1.0
        heading = math.fmod(self.state.yaw + direction * angular_delta,
                            2 * math.pi)
        r = self.attrs.L / 2
        self.state.x = self.state.x + r * (math.cos(self.state.yaw) -
                                           math.cos(heading))
        self.state.y = self.state.y + r * (math.sin(self.state.yaw) -
                                           math.sin(heading))
        self.state.yaw = heading

        ds = v * dt
        self.state.s += ds

    def on_update_sideway(self, dt):
        """on_update_sideway
        """
        v = math.fabs(self.state.velocity_x)
        v = clamp(v + self.state.acceleration_x * dt, 0.0, 20.47)
        if self.state.gear == 2:
            self.state.velocity_x = -v
        else:
            self.state.velocity_x = v
        heading = self.state.yaw
        dx = self.state.velocity_x * math.cos(heading + math.pi / 2) * dt
        dy = self.state.velocity_x * math.sin(heading + math.pi / 2) * dt
        self.state.x += dx
        self.state.y += dy
        ds = math.fabs(self.state.velocity_x) * dt
        self.state.s += ds

    def on_update_crabwalk(self, dt):
        """on_update_crabwalk
        """
        v = math.fabs(self.state.velocity_x)
        v = clamp(v + self.state.acceleration_x * dt, 0.0, 20.47)
        if self.state.gear == 2:
            self.state.velocity_x = -v
        else:
            self.state.velocity_x = v
        heading = self.state.yaw
        angular = math.fmod(heading + self.state.steering * math.pi / 180,
                            math.pi * 2)
        dx = self.state.velocity_x * math.cos(angular) * dt
        dy = self.state.velocity_x * math.sin(angular) * dt
        ds = math.fabs(self.state.velocity_x) * dt
        self.state.x += dx
        self.state.y += dy
        self.state.s += ds

    def on_update(self):
        """update_vehicle_attrs
        """
        dt = 0.001
        ticks = 0
        while self.running():
            ticks += 1

            if self.state.auto_driving == 1 and not self.paused:
                if ((self.state.motion_mode == 1
                     or self.state.motion_mode == 5)
                        and (self.state.gear == 4 or self.state.gear == 2)):
                    self.on_update_ackermann(dt)

                elif (self.state.motion_mode == 2
                      and (self.state.gear == 4 or self.state.gear == 2)):
                    self.on_update_spot_turn(dt)

                elif (self.state.motion_mode == 4
                      and (self.state.gear == 4 or self.state.gear == 2)):
                    self.on_update_sideway(dt)

                elif (self.state.motion_mode == 3
                      and (self.state.gear == 4 or self.state.gear == 2)):
                    self.on_update_crabwalk(dt)

            self.scr.world_win.draw('State', [
                f'ticks: {ticks} paused: {self.paused}',
                f'x: {self.state.x:.6f}',
                f'y: {self.state.y:.6f}',
                f'yaw: {self.state.yaw:.6f}'
                f' {math.degrees(self.state.yaw):.6f}',
                f'omega: {self.state.angular_rate_yaw:.6f}',
                f'vx: {self.state.velocity_x:.6f}',
                f'ax: {self.state.acceleration_x:.6f}',
                f's: {self.state.s:.6f}',
                f'steering: {self.state.steering}',
                f'steering_rate: {self.state.steering_rate}',
            ], curses.A_BOLD | curses.color_pair(1))

            time.sleep(dt)

    def mrf_to_vrf(self, orientation, mrf):
        """mrf_to_vrf
        """
        # mrf: vehicle axis
        # vrf: world axis
        # orientation: quaternion
        rotation = Rotation.from_quat(orientation)
        vrf = np.mat(rotation.inv().as_matrix()) * np.mat(mrf).T
        return [
            vrf.getA1()[0],
            vrf.getA1()[1],
            vrf.getA1()[2],
        ]

    def on_pose(self):
        """on_pose
        """
        seq = 0
        while self.running():
            seq += 1
            pose_msg = localization_pb2.LocalizationEstimate()
            pose_msg.Clear()
            pose_msg.header.timestamp_sec = time.time()
            pose_msg.header.module_name = 'SimpleVehicle'
            pose_msg.header.sequence_num = seq
            pose_msg.pose.position.x = self.state.x
            pose_msg.pose.position.y = self.state.y
            pose_msg.pose.position.z = self.state.z
            orientation = Rotation.from_euler(
                'xyz', [0, 0, self.state.yaw - math.pi / 2]).as_quat()
            pose_msg.pose.orientation.qx = orientation[0]
            pose_msg.pose.orientation.qy = orientation[1]
            pose_msg.pose.orientation.qz = orientation[2]
            pose_msg.pose.orientation.qw = orientation[3]
            pose_msg.pose.heading = self.state.yaw
            linear_velocity = [
                self.state.velocity_x * math.cos(self.state.yaw),
                self.state.velocity_x * math.sin(self.state.yaw),
                self.state.velocity_z,
            ]
            pose_msg.pose.linear_velocity.x = linear_velocity[0]
            pose_msg.pose.linear_velocity.y = linear_velocity[1]
            pose_msg.pose.linear_velocity.z = linear_velocity[2]
            linear_accel = [
                self.state.acceleration_x * math.cos(self.state.yaw),
                self.state.acceleration_x * math.sin(self.state.yaw),
                self.state.acceleration_z,
            ]
            pose_msg.pose.linear_acceleration.x = linear_accel[0]
            pose_msg.pose.linear_acceleration.y = linear_accel[1]
            pose_msg.pose.linear_acceleration.z = linear_accel[2]
            angular_velocity = [
                self.state.angular_rate_pitch,
                self.state.angular_rate_roll,
                self.state.angular_rate_yaw,
            ]
            pose_msg.pose.angular_velocity.x = angular_velocity[0]
            pose_msg.pose.angular_velocity.y = angular_velocity[1]
            pose_msg.pose.angular_velocity.z = angular_velocity[2]

            linear_accel_vrf = self.mrf_to_vrf(orientation, linear_accel)
            pose_msg.pose.linear_acceleration_vrf.x = linear_accel_vrf[0]
            pose_msg.pose.linear_acceleration_vrf.y = linear_accel_vrf[1]
            pose_msg.pose.linear_acceleration_vrf.z = linear_accel_vrf[2]

            angular_velocity_vrf = self.mrf_to_vrf(orientation,
                                                   angular_velocity)
            pose_msg.pose.angular_velocity_vrf.x = angular_velocity_vrf[0]
            pose_msg.pose.angular_velocity_vrf.y = angular_velocity_vrf[1]
            pose_msg.pose.angular_velocity_vrf.z = angular_velocity_vrf[2]

            self.pose_writer.write(pose_msg)
            time.sleep(0.01)

    def pause(self):
        """pause
        """
        self.paused = True

    def resume(self):
        """resume
        """
        self.paused = False

    def reset(self):
        """reset
        """
        self.state.x = self._init_args['initial_x']
        self.state.y = self._init_args['initial_y']
        self.state.yaw = self._init_args['initial_yaw']
        self.state.s = 0.0
        self.state.velocity_x = 0.0
        self.state.acceleration_x = 0.0
        self.state.angular_rate_yaw = 0.0
        self.state.steering = 0.0
        self.state.steering_rate = 0.0
        self.state.motion_mode = 1
        self.state.gear = 0

    def running(self):
        """running
        """
        return not self._stop_event.is_set()

    def run(self):
        """run
        """

        self.control = threading.Thread(target=self.on_control, )
        self.report = threading.Thread(target=self.on_report, )
        self.update = threading.Thread(target=self.on_update, )
        self.pose = threading.Thread(target=self.on_pose, )

        self.control.start()
        self.report.start()
        self.update.start()
        self.pose.start()

        self.control.join()
        self.report.join()
        self.update.join()
        self.pose.join()

    def shutdown(self):
        """shutdown
        """
        self._stop_event.set()


def main():
    """main entry
    """
    cyber.init()
    stdscr = curses.initscr()
    scr = screen.Screen(stdscr)
    vehicle = SimpleVehicle(scr, './vehicle.dbc', 'can0')

    def signal_handler(sig, frame):
        """signal_handler
        """
        print('exiting...')
        exit_signals = [signal.SIGINT, signal.SIGTERM]
        if sig in exit_signals:
            exit_event.set()
            vehicle.shutdown()
            cyber.shutdown()
        else:
            # unhandled signal
            print(f'Unhandled signal: {sig}', traceback.print_stack(frame))

    signal.signal(signal.SIGINT, signal_handler)

    try:
        vehicle.run()
    except KeyboardInterrupt:
        exit_event.set()
        vehicle.shutdown()
        cyber.shutdown()
    finally:
        exit_event.set()
        vehicle.shutdown()
        cyber.shutdown()


if __name__ == '__main__':
    main()
