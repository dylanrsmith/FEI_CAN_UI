import threading
import can
import os
import time
import sys
from datetime import datetime


class CAN_FEI:
    """
    This module contains all of the main functions for Sending and receiving CAN messages between the Pi and relay boards.
    """

    global can_bus
    global gd
    global time
    global i

    def __init__(self, ob):
        """
        Constructor Method for Creating an Instance of CAN_FEI

        NOTE: If using can0 instead of can0, make sure to change the channel in the can_bus constructor

        :param ob: Used to hold an instance of global_defines(Global Variables)
        """
        self.can_bus = can.interface.Bus(channel="can0", bustype="socketcan")
        self.gd = ob

    def flip_one(board, relay, state):
        """
        Sends a can message to change the state of a SINGLE relay

        :param board: Target Board Number to receive CAN message.
        :type board: int

        :param relay: Relay Number to be manipulated.
        :type relay: int
        :param state: State to set target relay to (on/off).
        :type state: int or boolean
        """
        can_bus = can.interface.Bus(channel="can0", bustype="socketcan")
        msg = can.Message(data=[0, 0, 0, 0, 0, 0, 0, 0], is_extended_id=True)

        board = int(board)
        relay = int(relay)
        state = int(state)
        msg.arbitration_id = (0x18DA << 8 | board) << 8 | 0xF9
        msg.data[7] = relay
        msg.data[6] = state

        can_bus.send(msg)

    def ping(self):
        """
        Sends a CAN message where 5th byte is 1, asking for a request from any online relay boards.

        Relay board should return same message, when response is received, that board will be updated as ready.

        Handled by a thread.
        """
        boards = self.gd.board_list
        ping_msg = can.Message(data=[0, 0, 0, 1, 0, 0, 0, 0], is_extended_id=True)
        thread = can.ThreadSafeBus(channel="can0", bustype="socketcan")
        for i in boards:
            ping_msg.arbitration_id = ((0x18DA << 8) | i) << 8 | 0xF9
            thread.send(ping_msg)
            time.sleep(0.05)

        time.sleep(0.5)

        for board in self.gd.time_dict:
            # Update board to be offline if last response was received over 30 seconds ago:
            if (
                (time.time() - self.gd.time_dict[board]) > 35.0
                and board in self.gd.ping_dict
                and self.gd.ping_dict[board] != 0
            ):
                self.gd.ping_dict.update({int(board): 0})
                print("Dictionary : " + str(self.gd.ping_dict.copy()))

    def flip_all_on(self, n):
        """
        Activates all relays on specified board.

        :param n: Board Number to receive CAN message.
        :type n: int
        """
        can_bus = can.interface.Bus(channel="can0", bustype="socketcan")
        msg = can.Message(data=[0, 0, 0, 0, 0, 0, 4, 0], is_extended_id=True)

        id_prefix = 0x18DA
        id_suffix = 0xF9
        board_num = int(n)

        msg.arbitration_id = (id_prefix << 8 | board_num) << 8 | id_suffix
        can_bus.send(msg)

    def flip_all_off(self, n):
        """
        Deacivates all relays on specified board.

        :param n: Board Number to receive CAN message
        :type n: int
        """
        can_bus = can.interface.Bus(channel="can0", bustype="socketcan")
        msg = can.Message(data=[0, 0, 0, 0, 0, 0, 5, 0], is_extended_id=True)

        id_prefix = 0x18DA
        id_suffix = 0xF9
        board_num = int(n)

        msg.arbitration_id = (id_prefix << 8 | board_num) << 8 | id_suffix
        can_bus.send(msg)

    def flip_loop(self, x):
        """
        Will toggle all relays on and then off, for a specified amount of intervals.

        NOTE: Board Number is hard coded in the Message Constructor.

        :param x: Number of loops the relays will be toggled.
        :type x: int
        """
        for i in range(x):
            msg2 = can.Message(
                arbitration_id=0x18DA02F9,
                data=[0, 0, 0, 0, 0, 0, 4, 0],
                is_extended_id=True,
            )
            msg3 = can.Message(
                arbitration_id=0x18DA02F9,
                data=[0, 0, 0, 0, 0, 0, 5, 0],
                is_extended_id=True,
            )

            self.can_bus.send(msg2)
            # time.sleep(4)
            self.can_bus.send(msg3)
            # time.sleep(4)

    def receive_CAN_while(self):
        """
        Method for receiving and deciphering CAN.

        Baud Rate: 250,000
        """
        filters = [{"can_id": 0x18DAF901, "can_mask": 0x18DAF900, "extended": True}]
        thread_bus = can.ThreadSafeBus(
            channel="can0", bustype="socketcan", can_filters=filters
        )

        while True:
            message = thread_bus.recv(timeout=1)
            time_recv = time.time()

            if message != None:
                board = message.arbitration_id >> 0 & 0xFF

                if message.is_extended_id == True:
                    self.gd.time_dict.update({int(board): time_recv})

                    if board not in self.gd.ping_dict or self.gd.ping_dict[board] != 1:
                        self.gd.ping_dict.update({int(board): 1})
                        print("Dictionary : " + str(self.gd.ping_dict.copy()))

            time.sleep(0)

    def ping_thread(self):
        """
        Thread to handle periodic sending of polling messages.

        Uses a threading Timer to run every 30 seconds.
        """
        self.ping()
        threading.Timer(30, self.ping_thread).start()

    def start_thread(self):
        """
        Function to start Send and receiving threads.
        """
        self.ping_thread()
        while_thread = threading.Thread(target=self.receive_CAN_while)
        while_thread.start()


# TEST ENVIRONMENT:
# can0 = CAN_FEI(0)

# can0.flip_loop(100)
