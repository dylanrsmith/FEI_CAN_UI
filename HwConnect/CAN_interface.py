import can
import time
import threading
from threading import *


class CANbus(can.Listener):
    global _can

    def __init__(self, canbus, msg_buffer, ob):
        self.msg_buffer = msg_buffer
        self.last_message_time = 0
        self.canbus = canbus
        self.setup()
        self._can = ob

    def setup(self):
        self.notifier = can.Notifier(self.canbus, [self])

    def on_message_received(self, msg):
        """

        :param msg:
        """
        if (
            (msg.arbitration_id == 0x18FFE277)
            or (msg.arbitration_id == 0x18FF7527)
            or (msg.arbitration_id == 0x18FF6476)
            or (msg.arbitration_id == 0x18FF0975)
        ):
            self.msg_buffer.appendleft(msg)
            self.last_message_time = time.time()

    #             print('msg in buffer1')

    def msgreceive(self, msg_id, index, bytenr, explevel, mask):
        """

        :param msg_id:
        :param index:
        :param bytenr:
        :param explevel:
        :param mask:
        """
        notReceived = 1
        while notReceived:
            if self._can.msg_buffer:
                msg = self._can.msg_buffer.pop()
                if msg.arbitration_id == 0x18FFE277:
                    data = msg.data
                    ERPM = (data[3] << 8) + data[2]
                    self._can.current_spd = int(ERPM)
                if msg.arbitration_id == 0x18FF7527:
                    data = msg.data
                    self._can.reverserEngaged = data[4] & 0x01
                    self._can.feederreverserEngaged = data[4] & 0x05
                if msg.arbitration_id == 0x18FF6476:
                    data = msg.data
                    self._can.ThreshingRotorStatus = data[4] & 0x1C
                if msg.arbitration_id == 0x18FF0975:
                    data = msg.data
                    self._can.ThreshingFeederStatus = data[7] & 0x70

            else:
                notReceived = 0

    def RecvCAN(self):
        self.msgreceive(0x18FFE277, -1, 0, 0, 0)
        threading.Timer(0.01, self.RecvCAN).start()
