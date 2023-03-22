import itertools
import tkinter as tk
from tkinter import ttk
from functools import partial
import threading
import psutil
from HwConnect.CAN_FEI import *


class update_ui:
    global _ui, io_ob

    def __init__(self, ob1):
        """
        This module handles all updating of UI widgets and displayed values
        :param ob1: Set to _ui...references global_defines
        :param ob2: Set to io_ob...initially referenced IO_Ctrl(deprecated)
        """
        self._ui = ob1
        self._ge = ob1
        self.can2 = CAN_FEI(ob1)
        self.label_refresh_rate = 0

    def update_ui_dict(self):
        for key in self._ui.UI_dict:
            if self._ui.testing_active == 0:
                val = self.io_ob.data_read(key)
            else:
                if self._ui.toggle == 0:
                    val = 1
                else:
                    val = 0

            self._ui.UI_dict.update({key: val})
        if self._ui.testing_active == 1:
            if self._ui.toggle == 0:
                self._ui.toggle = 1
            else:
                self._ui.toggle = 0

        self.update_ui_spn()

    def update_ui_spn(self):
        """
        Function to update UI based on dictionary data.

        Tied to First 7 SPN Tabs.

        This is what causes the buttons to flash red and green in testing mode.
        """
        for key in self._ui.UI_dict:
            data = self._ui.UI_dict[key]
            # self._ge.dig_ip_button.append(0)

            try:
                # DIG I/P

                if key in self._ui.dig_ip_spn:
                    ind = self._ui.dig_ip_spn.index(key)
                    if self._ui.dig_state[key] == 1:
                        self._ui.dig_ip_button[ind].config(bg="Green")
                    else:
                        self._ui.dig_ip_button[ind].config(bg="Red")  # runtime error
                    # i = ind
                    # if i < 19:
                    #     self._ui.dig_ip_button[i].grid(row=i, column=1)
                    # else:
                    #     self._ui.dig_ip_button[i].grid(row=i - 19, column=4)

                # DIG O/P
                # elif key in self._ui.dig_op_spn:
                #     ind = self._ui.dig_op_spn.index(key)  # find position of that spn
                #     if data == 1:
                #         self._ui.dig_op_button[ind].config(bg="Green")
                #     else:
                #         self._ui.dig_op_button[ind].config(bg="Red")
                #     i = ind
                #     if 0 <= i < 31:
                #         row = i
                #         column = 1
                #     elif 31 <= i < 62:
                #         row = i - 31
                #         column = 3
                #     elif 62 <= i < 94:
                #         row = i - 62
                #         column = 5
                #     self._ui.dig_op_button[i].grid(row=row, column=column + 2)

                # Update Voltage Tab
                elif key in self._ui.vol_ip_spn:
                    ind = self._ui.vol_ip_spn.index(key)

                    i = ind
                    # if i < 29:
                    #     self._ui.volt_label[i].grid(row=i, column=1)
                    # else:
                    #     self._ui.volt_label[i].grid(row=i - 29, column=5)

                    if self._ui.SimMode == 1:
                        if self._ui.volt_state[key] == 1:
                            self._ui.volt_toggle[ind].config(bg="Green")
                        else:
                            self._ui.volt_toggle[ind].config(bg="Red")

                    self._ui.volt_label[ind].delete(0, 100)
                    self._ui.volt_label[ind].insert(0, data)

                #Update PWM I/P tab
                elif key in self._ui.pwm_ip_spn:
                    ind = self._ui.pwm_ip_spn.index(key)
                    self._ui.pwm_ip_label[ind].delete(0, 100)
                    self._ui.pwm_ip_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.pwm_state[key] == 1:
                            self._ui.pwm_ip_toggle[ind].config(bg="Green")
                        else:
                            self._ui.pwm_ip_toggle[ind].config(bg="Red")

                # # Update PWM O/P tab
                # elif key in self._ui.pwm_op_spn:
                #     ind = self._ui.pwm_op_spn.index(key)
                #     self._ui.pwm_op_label[ind].delete(0, 100)
                #     self._ui.pwm_op_label[ind].insert(0, data)

                # Update Freq Tab
                elif key in self._ui.fq_ip_spn:
                    ind = self._ui.fq_ip_spn.index(key)
                    self._ui.freq_label[ind].delete(0, 100)
                    self._ui.freq_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.freq_state[key] == 1:
                            self._ui.freq_toggle[ind].config(bg="Green")
                        else:
                            self._ui.freq_toggle[ind].config(bg="Red")

                # Update Pulse tab
                elif key in self._ui.pulse_spn:
                    ind = self._ui.pulse_spn.index(key)
                    self._ui.pulse_label[ind].delete(0, 100)
                    self._ui.pulse_label[ind].insert(0, data)

                    if self._ui.SimMode == 1:
                        if self._ui.pulse_state[key] == 1:
                            self._ui.pulse_toggle[ind].config(bg="Green")
                        else:
                            self._ui.pulse_toggle[ind].config(bg="Red")

            except RuntimeError: 
                pass
    def update_settings(self):
        """
        Updates Color Of Settings Buttons depending on their linked value.
        """
        all_widgets = list(
            itertools.chain(
                self._ui.dig_ip_option,
                self._ui.open_option,
                self._ui.volt_toggle,
                self._ui.pwm_ip_toggle,
                self._ui.freq_toggle,
                self._ui.pulse_toggle,
                self._ui.actuator_load,
                self._ui.actuator_set,
            )
        )
        if self._ui.KeyIsON == 1:
            self._ui.Key_Button.config(bg="Green")
        elif self._ui.KeyIsON == 0:
            self._ui.Key_Button.config(bg="Red")

        if self._ui.debug_mode == 0:
            self._ui.debug_mode_button.config(bg="Red")
        elif self._ui.debug_mode == 1:
            self._ui.debug_mode_button.config(bg="Green")

    def update_cc_console(self):
        if self._ui.thresher_engage_state == 0:
            self._ui.thresher_engage_button.config(bg="Red")
        else:
            self._ui.thresher_engage_button.config(bg="Green")

        if self._ui.feeder_engage_state == 0:
            self._ui.feeder_engage_button.config(bg="Red")
        else:
            self._ui.feeder_engage_button.config(bg="Green")

    def update_cpu(self):
        """
        Displays CPU usage under Settings tab

        Uses 'psutil'
        """
        if self._ui.fei_compatible == 1:
            cpu = str(psutil.cpu_percent(0.5)) + "%"
            self._ui.cpu_entry.delete(0, 100)
            self._ui.cpu_entry.insert(0, cpu)

    def update_ui_offline(self):
        """
        Part of ui_update thread.

        Checks to see if any boards are offline. If so, linked UI widgets will be disabled.
        """
        for bno in self._ui.board_wid_dict:
            online = 0
            if bno in self._ui.ping_dict and self._ui.ping_dict[bno] == 1:
                online = 1

            for widg in self._ui.board_wid_dict[bno]:
                try:
                    if online:
                        widg.config(state=tk.NORMAL)
                    else:
                        #widg.config(state=tk.DISABLED)
                        widg.config(state=tk.NORMAL)
                        if widg.__class__.__name__ != "OptionMenu":
                            widg.config(bg="azure3")
                except AttributeError:
                    print("Encountered AttributeError in update_ui_offline")

    def mainloop(self):
        """
        Holds Tkinter .mainloop()

        Main function for running UI.

        DO NOT REMOVE
        """
        tk.mainloop()
