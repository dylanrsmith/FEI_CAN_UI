"""
#   Writing 1 = off
#   Writing 0 = on
#
#   Open   Close  Status
#   (257)  (263)
#     0      1    Open 
#     1      0    Close
"""
# from IOCtrl import *
import time

ghcv_init_flag = 0


class ghcv_plant:
    global _gh, _io

    def __init__(self, ob1, ob2):
        self._gh = ob1
        self._io = ob2

    def ghcv_init(self):
        self._io.data_to_board(257, int(0))  # Default Open for GNSS testing
        self._io.data_to_board(
            263, int(1)
        )  # Remove and uncomment two lines below afterwards
        self._gh.cover_open_sensor = 1  # Update status of open sol for GUI
        self._gh.cover_close_sensor = 0  # Update status of closed sol for GUI

    def calculate_state(self):
        global ghcv_init_flag
        if ghcv_init_flag == 0:
            self.ghcv_init()  # to set intial status to covers closed
            ghcv_init_flag = 1

        self._gh.iscoveropenactive = self._io.data_read(380)  # Read cover open sol
        self._gh.iscoverclosedactive = self._io.data_read(381)  # Read cover close sol

        if (
            self._gh.ghcv_enabled
        ):  # To enable or disable the plant module from GUI section Plant Model UCM2
            if self._gh.testing_active == 0:
                if (
                    self._gh.iscoveropenactive == 1
                    and self._gh.iscoverclosedactive == 0
                ):  # only process data if state/edge is changed
                    # Covers Open Edge
                    if self._gh.g_opened_tmr_ms_u16 > 0:  # Decrement cover open counter
                        self._gh.g_opened_tmr_ms_u16 -= 1
                    if (
                        self._gh.open_error != 1 and self._gh.g_opened_tmr_ms_u16 == 0
                    ):  # if no open error set from GUI and open counter is 0
                        self._gh.g_closed_tmr_ms_u16 = (
                            self._gh.g_tmr_max_val_ms_u32
                        )  # Reset counters
                        self._gh.g_opened_tmr_ms_u16 = self._gh.g_tmr_max_val_ms_u32
                        self._gh.cover_open_sensor = (
                            1  # Update status of open sol for GUI
                        )
                        self._gh.cover_close_sensor = (
                            0  # Update status of closed sol for GUI
                        )
                        self._io.data_to_board(
                            257, int(0)
                        )  # Update status of open sol sensor
                        self._io.data_to_board(
                            263, int(1)
                        )  # Update status of closed sol sensor

                if (
                    self._gh.iscoveropenactive == 0
                    and self._gh.iscoverclosedactive == 1
                ):  # only process data if state/edge is changed
                    # Covers Close Edge
                    if (
                        self._gh.g_closed_tmr_ms_u16 > 0
                    ):  # Decrement cover close counter
                        self._gh.g_closed_tmr_ms_u16 -= 1
                    if (
                        self._gh.close_error != 1 and self._gh.g_closed_tmr_ms_u16 == 0
                    ):  # if no close error set from GUI and close counter is 0
                        self._gh.g_closed_tmr_ms_u16 = (
                            self._gh.g_tmr_max_val_ms_u32
                        )  # Reset counters
                        self._gh.g_opened_tmr_ms_u16 = self._gh.g_tmr_max_val_ms_u32
                        self._gh.cover_open_sensor = (
                            0  # Update status of open sol for GUI
                        )
                        self._gh.cover_close_sensor = (
                            1  # Update status of closed sol for GUI
                        )
                        self._io.data_to_board(
                            257, int(1)
                        )  # Update status of open sol sensor
                        self._io.data_to_board(
                            263, int(0)
                        )  # Update status of closed sol sensor


# def calculate_timer(self):
#     #call this function in a thread
#     if self._gh.ghcv_enabled:
#         if self._gh.testing_active == 0:
#             self._gh.iscoveropenactive = self._io.data_read(380)
#         if self._gh.iscoveropenactive:
#             if self._gh.g_opened_tmr_ms_u16 > 0:
#                 self._gh.g_opened_tmr_ms_u16 -= 1
#             self._gh.g_closed_tmr_ms_u16 = self._gh.g_tmr_max_val_ms_u32
#         if self._gh.testing_active == 0:
#             self._gh.iscoverclosedactive = self._io.data_read(381)
#             #print("Close :",self._io.data_read(381))
#         if self._gh.iscoverclosedactive:
#             if self._gh.g_closed_tmr_ms_u16 > 0:
#                 self._gh.g_closed_tmr_ms_u16 -=1
#             self._gh.g_opened_tmr_ms_u16 = self._gh.g_tmr_max_val_ms_u32


#         self.calculate_timer()
#         if self._gh.open_error != 1:
#             if self._gh.g_opened_tmr_ms_u16 == 0:
#                 self._gh.cover_open_sensor = 1
#                 self._gh.cover_open.set(0)
#             else:
#                 self._gh.cover_open_sensor = 0
#         else:
#             self._gh.cover_open_sensor = 0
#         if self._gh.testing_active == 0:
#             self._io.data_to_board(257, self._gh.cover_open_sensor)
#         if self._gh.close_error != 1:
#             if self._gh.g_closed_tmr_ms_u16 == 0:
#                 self._gh.cover_close_sensor = 1
#                 self._gh.cover_closed.set(0)
#             else:
#                 self._gh.cover_close_sensor = 0
#         else:
#             self._gh.cover_close_sensor = 0
#         if self._gh.testing_active == 0:
#             self._io.data_to_board(263, self._gh.cover_close_sensor)
#         print(self._gh.iscoveropenactive, self._gh.cover_open_sensor, self._gh.iscoverclosedactive, self._gh.cover_close_sensor)
