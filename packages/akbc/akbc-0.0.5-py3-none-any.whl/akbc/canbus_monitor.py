#!/usr/bin/env python
"""canbus monitor
"""
import threading
import time

import can
import cantools
import cantools.database
import cantools.database.can.database


class CanbusMonitor:
    """CanbusMonitor
    """

    def __init__(self, dbc_file, device):
        """__init__
        """
        self.db = cantools.database.load_file(dbc_file)
        self.canbus = can.Bus(
            interface='socketcan',
            channel=device,
            bitrate=500000,
        )

        self.canbus_messages = {}
        self.canbus_message_data = {}
        self.canbus_counter = {}
        self.canbus_last = {}
        self.canbus_latency = {}

        self.threads = []
        self._stop_event = threading.Event()

    def on_canbus(self):
        """on_canbus
        """
        while self.running():
            message = self.canbus.recv(1)
            if message is None:
                continue
            available_messages = list(
                map(lambda x: x.frame_id, self.db.messages))
            if message.arbitration_id in available_messages:
                if message.arbitration_id not in self.canbus_counter:
                    self.canbus_counter[message.arbitration_id] = 0
                self.canbus_counter[message.arbitration_id] += 1
                if message.arbitration_id not in self.canbus_last:
                    self.canbus_last[message.arbitration_id] = 0
                last = self.canbus_last[message.arbitration_id]
                now = time.time()
                self.canbus_last[message.arbitration_id] = now
                latency = (now - last) * 1000
                self.canbus_latency[message.arbitration_id] = latency
                spec = self.db.get_message_by_frame_id(message.arbitration_id)
                data = spec.decode(message.data)
                self.canbus_messages[message.arbitration_id] = message
                self.canbus_message_data[message.arbitration_id] = data

    def get_showing_text(self):
        """get_showing_text
        """
        content = []
        for message in self.canbus_messages.values():
            if not message:
                continue
            spec = self.db.get_message_by_frame_id(message.arbitration_id)
            if not spec:
                continue
            content.append(f'{hex(spec.frame_id)}: '
                           f'{spec.length} '
                           f'{self.canbus_counter[spec.frame_id]:6} '
                           f'{self.canbus_latency[spec.frame_id]:8.3f} '
                           f'{message.data.hex()} {spec.name}')
            content.append(f'    {self.canbus_message_data[spec.frame_id]}')
        return content

    def running(self):
        """running
        """
        return not self._stop_event.is_set()

    def run(self):
        canbus_thread = threading.Thread(target=self.on_canbus)
        self.threads.append(canbus_thread)
        canbus_thread.start()

        canbus_thread.join()

    def shutdown(self):
        """shutdown
        """
        self._stop_event.set()
