import tkinter as tk
from tkinter import ttk
from functools import partial
from UserInterface.update_ui import *
from UserInterface.ui_callbacks import *
from global_defines import *
from HwConnect.CAN_FEI import *


class generate_ui:
    """
    This module is responsible for initializing each component of the UI, as well as it's grid placement.
    """

    global _ge, ui, ui_call

    def __init__(self, ob1):
        """
        Constructor used to create an instance of generate_ui.

        :param ob1 (Object): Used to pass an instance of global_defines.
        :param ob2 (Object): Used to pass an instance of IOCtrl.
        """
        self._ge = ob1
        self.ui = update_ui(self._ge)
        self.ui_call = ui_callbacks(self._ge)
        self._ge.dig_ip_options = ["Open_Circuit"]
        self._ge.can2 = CAN_FEI(ob1)

    # Generates first 7 UI Tabs
    def generate_spn_ui(self):
        """
        The function `generate_spn_ui` is responsible for creating these UI tabs and their widgets:

        DIG I/P | DIG O/P | VOLTAGE | PWM I/P | PWM O/P | Freq | Pulse
        """
        # Digital Input Tab
        for i in range(len(self._ge.dig_ip_spn)):
            self._ge.dig_ip_button.append(0)
            self._ge.dig_ip_option.append(0)
            self._ge.dig_ip_option_var.append(tk.StringVar())

            self._ge.dig_ip_button[i] = tk.Button(
                self._ge.dig_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.dig_ip_callback, i),
            )

            self._ge.dig_ip_option[i] = tk.OptionMenu(
                self._ge.dig_ip_frame,
                self._ge.dig_ip_option_var[i],
                *self._ge.dig_ip_options,
                command=partial(self.ui_call.output_send, self._ge.dig_ip_spn[i])
            )

            label = tk.Label(
                self._ge.dig_ip_frame,
                text=self._ge.dig_ip_name[i],
                bg="azure3",
                width=55,
            )

            self._ge.dig_ip_mode.update({i: 0})

            spn = self._ge.dig_ip_spn[i]
            bno = self._ge.board_dict[spn]

            tempList = []
            if bno in self._ge.board_wid_dict:
                tempList = self._ge.board_wid_dict[bno]

            tempList.append(self._ge.dig_ip_option[i])

            self._ge.board_wid_dict.update({bno: tempList})

            # first column
            if i < 19:
                label.grid(row=i, column=0)
                #self._ge.dig_ip_button[i].grid(row=i, column=1) #not needed for can_fei
                # If Board and Channel are configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i, column=2)
            # second column
            else:
                label.grid(row=i - 19, column=3)
                #self._ge.dig_ip_button[i].grid(row=i - 19, column=4)
                # If Board and Channel are configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.dig_ip_option[i].grid(row=i - 19, column=5)

        # Digital Output Tab
        # for i in range(len(self._ge.dig_op_spn)):
        #     self._ge.dig_op_button.append(0)
        #     self._ge.dig_op_button[i] = tk.Button(
        #         self._ge.dig_op_frame,
        #         height=1,
        #         width=4,
        #         bd=6,
        #         fg="black",
        #         font=("Geneva", 6),
        #         bg="Green",
        #     )
        #     label = tk.Label(
        #         self._ge.dig_op_frame,
        #         text=self._ge.dig_op_name[i],
        #         bg="azure3",
        #         width=50,
        #     )
        #     if 0 <= i < 31:
        #         row = i
        #         column = 1
        #     elif 31 <= i < 62:
        #         row = i - 31
        #         column = 3
        #     elif 62 <= i < 94:
        #         row = i - 62
        #         column = 5
        #     label.grid(row=row, column=column + 1)
        #     self._ge.dig_op_button[i].grid(row=row, column=column + 2)

        # Voltage Tab
        for i in range(len(self._ge.vol_ip_spn)):  # length = 58
            self._ge.volt_label.append(0)
            self._ge.volt_button.append(0)
            self._ge.volt_toggle.append(0)
            self._ge.relay_switch.append(1)
            self._ge.volt_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.volt_ip_frame,
                text=self._ge.vol_ip_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.volt_label[i] = tk.Entry(
                self._ge.volt_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.volt_string[i],      # enables toggling input box 0-1
            )
            self._ge.volt_button[i] = tk.Button(
                self._ge.volt_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.buttonVolt, i),
            )
            self._ge.volt_toggle[i] = tk.Button(
                self._ge.volt_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Red",
                command=partial(self.ui_call.voltToggle, i),
            )

            if i < 29:
                label.grid(row=i, column=0)
                #self._ge.volt_label[i].grid(row=i, column=1)
                #self._ge.volt_button[i].grid(row=i, column=2)
                # If excel has board configured.
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.volt_toggle[i].grid(row=i, column=3)
            else:
                label.grid(row=i - 29, column=4)
                #self._ge.volt_label[i].grid(row=i - 29, column=5)
                #self._ge.volt_button[i].grid(row=i - 29, column=6)
                # If excel has board configured
                if self._ge.bool_both.get(self._ge.vol_ip_spn[i]):
                    self._ge.volt_toggle[i].grid(row=i - 29, column=7)

            #self._ge.volt_label[i].insert(0, "0")

        # PWM Input Tab
        for i in range(len(self._ge.pwm_ip_spn)):
            self._ge.pwm_ip_label.append(0)
            self._ge.pwm_ip_button.append(0)
            self._ge.pwm_ip_toggle.append(0)
            self._ge.pwm_ip_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.pwm_ip_frame,
                text=self._ge.pwm_ip_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.pwm_ip_label[i] = tk.Entry(
                self._ge.pwm_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.pwm_ip_string[i],
            )

            # Create a Button widget for update
            self._ge.pwm_ip_button[i] = tk.Button(
                self._ge.pwm_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.buttonPwmip, i),
            )
            label.grid(row=i, column=0)
            #self._ge.pwm_ip_label[i].grid(row=i, column=1)
            #self._ge.pwm_ip_button[i].grid(row=i, column=2)
            self._ge.pwm_ip_label[i].insert(0, "0")

            # Create a Button for toggling relay, based on excel configuration
            self._ge.pwm_ip_toggle[i] = tk.Button(
                self._ge.pwm_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.pwmToggle, i),
            )
            if self._ge.bool_both.get(self._ge.pwm_ip_spn[i]):
                self._ge.pwm_ip_toggle[i].grid(row=i, column=3)

        # PWM Output Tab
        for i in range(len(self._ge.pwm_op_spn)):
            self._ge.pwm_op_label.append(0)
            label = tk.Label(
                self._ge.pwm_op_frame,
                text=self._ge.pwm_op_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.pwm_op_label[i] = tk.Entry(
                self._ge.pwm_op_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
            )
            label.grid(row=i, column=0)
            self._ge.pwm_op_label[i].grid(row=i, column=1)
            self._ge.pwm_op_label[i].insert(0, "0")

        # Freq Tab
        for i in range(len(self._ge.fq_ip_spn)):
            self._ge.freq_label.append(0)
            self._ge.freq_button.append(0)
            self._ge.freq_toggle.append(0)
            self._ge.freq_string.append(tk.StringVar())
            label = tk.Label(
                self._ge.freq_ip_frame,
                text=self._ge.fq_ip_name[i],
                bg="azure3",
                width=55,
            )
            self._ge.freq_label[i] = tk.Entry(
                self._ge.freq_ip_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.freq_string[i],
            )
            self._ge.freq_button[i] = tk.Button(
                self._ge.freq_ip_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.buttonFreq, i),
            )
            label.grid(row=i, column=0)
            #self._ge.freq_label[i].grid(row=i, column=1)
            #self._ge.freq_button[i].grid(row=i, column=2)
            self._ge.freq_label[i].insert(0, "0")
            self._ge.freq_toggle[i] = tk.Button(
                self._ge.freq_ip_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.freqToggle, i),
            )

            if self._ge.bool_both.get(self._ge.fq_ip_spn[i]):
                self._ge.freq_toggle[i].grid(row=i, column=3)

        # Pulse Tab
        for i in range(len(self._ge.pulse_spn)):
            self._ge.pulse_label.append(i)
            self._ge.button_pulse.append(0)
            self._ge.pulse_toggle.append(0)
            self._ge.pulse_string.append(0)
            self._ge.pulse_string[i] = tk.StringVar()

            label = tk.Label(
                self._ge.pulse_frame, text=self._ge.pulse_name[i], bg="azure3", width=55
            )
            self._ge.pulse_label[i] = tk.Entry(
                self._ge.pulse_frame,
                bd=2,
                validate="key",
                width=6,
                font=("courier", 10),
                textvariable=self._ge.pulse_string[i],
            )
            self._ge.button_pulse[i] = tk.Button(
                self._ge.pulse_frame,
                height=1,
                width=11,
                bd=8,
                fg="white",
                font=("Geneva", 6),
                text="Update",
                bg="Steel Blue",
                command=partial(self.ui_call.buttonPulse, i),
            )
            label.grid(row=i, column=0)
            #self._ge.pulse_label[i].grid(row=i, column=1)
            #self._ge.button_pulse[i].grid(row=i, column=2)
            #self._ge.pulse_label[i].insert(0, "0")
            self._ge.pulse_toggle[i] = tk.Button(
                self._ge.pulse_frame,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="Green",
                command=partial(self.ui_call.pulseToggle, i),
            )

            if self._ge.bool_both.get(self._ge.fq_ip_spn[i]):
                self._ge.pulse_toggle[i].grid(row=i, column=3)

    def get_sim_mode(self):
        """
        When called, will read save state of Simulator Mode, and will disable/enable all widgets depending on value.

        Value is stored in SimMode.txt (0 or 1)
        """
        if self._ge.SimMode == 0:
            all_widgets = list(
                itertools.chain(
                    self._ge.dig_ip_option,
                    self._ge.open_option,
                    self._ge.volt_toggle,
                    self._ge.pwm_ip_toggle,
                    self._ge.freq_toggle,
                    self._ge.pulse_toggle,
                    self._ge.actuator_load,
                    self._ge.actuator_set,
                )
            )
            self._ge.sim_button.config(bg="Red")
            # for i in range(len(all_widgets)):
            #     try:
            #         all_widgets[i].config(state=tk.DISABLED)
            #         all_widgets[i].config(bg="azure3")
            #     except AttributeError:
            #         pass
            for i in range(80):
                self._ge.can2.flip_all_on(i)
        else:
            self._ge.sim_button.config(bg="Green")
            # for i in range(80):
            #     self._ge.can2.flip_all_off(i)

    # Open_To Tab:
    def generate_open_ui(self):
        """
        Function for generating components in the 'Open' UI tab

        Will Show Configured SPN's with a drop down menu to select open configuration.

        Searches for 'Open_to' value in column D of `config_sheet.xlsx`

        Value should either be B(open to battery), G(open to ground) or Both(where we can select between B or G in the UI, not open to both at the same time)
        """
        for i in range(len(self._ge.dig_ip_spn)):
            self._ge.open_option_var.append(tk.StringVar())
            self._ge.open_option.append(0)
            self._ge.open_button.append(0)
            x = self._ge.dig_ip_spn[i]
            parse = self._ge.ground_dict.get(x)
            self._ge.battery_option = ["Battery"]
            self._ge.ground_option = ["Ground"]
            self._ge.both_option = ["Battery", "Ground"]

            try:
                label = tk.Label(
                    self._ge.open_frame,
                    text=self._ge.dig_ip_name[i],
                    bg="azure3",
                    width=55,
                )
                self._ge.open_button[i] = tk.Button(
                    self._ge.open_frame,
                    text="Update",
                    fg="white",
                    bg="Steel Blue",
                    command=partial(
                        self.ui_call.open_button_callback, self._ge.dig_ip_spn[i]
                    ),
                )  # TODO, command=self.ui_call.callback) #Might have to make button list

                # Check each SPN value of column D in config_sheet

                if parse == "B":
                    self._ge.open_option[i] = tk.OptionMenu(
                        self._ge.open_frame,
                        self._ge.open_option_var[i],
                        *self._ge.battery_option,
                        command=partial(
                            self.ui_call.output_send, self._ge.dig_ip_spn[i]
                        )
                    )
                elif parse == "G":
                    self._ge.open_option[i] = tk.OptionMenu(
                        self._ge.open_frame,
                        self._ge.open_option_var[i],
                        *self._ge.ground_option,
                        command=partial(
                            self.ui_call.output_send, self._ge.dig_ip_spn[i]
                        )
                    )
                elif parse == "Both":
                    self._ge.open_option[i] = tk.OptionMenu(
                        self._ge.open_frame,
                        self._ge.open_option_var[i],
                        *self._ge.both_option,
                        command=partial(
                            self.ui_call.output_send, self._ge.dig_ip_spn[i]
                        )
                    )

                if self._ge.bool_all.get(self._ge.dig_ip_spn[i]):
                    label.grid(row=i, column=0)
                    # self._ge.open_button[i].grid(row=i,column=2)
                    self._ge.open_option[i].grid(row=i, column=1)

            except IndexError:
                label.grid(row=i, column=0)

    # Actuator Tab
    def generate_actuator_ui(self):
        """
        Generates Widgets under 'Actuator' UI Tab.

        actuator_dict={1:"act1",2:"act2",3:"act3"}  #Dictionary with Actuator # : Actuator Name pair
        actuator_label=[]
        actuator_load=[]
        actuator_pos=[]
        actuator_set=[]
        actuator_btn=[]
        """
        for i in range(len(self._ge.actuator_dict)):
            self._ge.actuator_label.append(0)
            self._ge.actuator_load.append(0)
            self._ge.actuator_pos.append(0)
            self._ge.actuator_set.append(0)
            self._ge.actuator_btn.append(0)

            try:
                if i == 0:
                    tk.Label(self._ge.actuator_frame, text="Load", width=20).grid(
                        row=i, column=1
                    )
                    tk.Label(
                        self._ge.actuator_frame, text="Actual Position", width=20
                    ).grid(row=i, column=2)
                    tk.Label(
                        self._ge.actuator_frame, text="Set Position", width=20
                    ).grid(row=i, column=3)
                else:
                    label = tk.Label(
                        self._ge.actuator_frame,
                        text=self._ge.actuator_dict[i],
                        bg="azure3",
                        width=15,
                    )
                    label.grid(row=i, column=0)
                    self._ge.actuator_load[i] = tk.Entry(
                        self._ge.actuator_frame, width=15
                    )
                    self._ge.actuator_load[i].grid(row=i, column=1)
                    self._ge.actuator_pos[i] = tk.Entry(
                        self._ge.actuator_frame, bg="azure3", width=15
                    )
                    self._ge.actuator_pos[i].grid(row=i, column=2)
                    self._ge.actuator_set[i] = tk.Entry(
                        self._ge.actuator_frame, width=15
                    )
                    self._ge.actuator_set[i].grid(row=i, column=3)
                    self._ge.actuator_btn[i] = tk.Button(
                        self._ge.actuator_frame,
                        text="Update",
                        fg="white",
                        bg="Steel Blue",
                    )  # TODO,command=)
                    self._ge.actuator_btn[i].grid(row=i, column=4)
            except KeyError:
                pass

    # Driveline Tab
    def generate_driveline_ui(self):
        for i in range(len(self._ge.sp_name)):
            self._ge.drive_label.append(0)
            label = tk.Label(
                self._ge.driveline_frame,
                text=self._ge.sp_name[i],
                bg="azure3",
                width=40,
            )
            label.grid(row=i, column=0)

            self._ge.drive_label[i] = tk.Entry(
                self._ge.driveline_frame, bd=2, font=("courier", 10)
            )
            self._ge.drive_label[i].grid(row=i, column=1)
            self._ge.drive_label[i].insert(0, "0")

        label = tk.Label(
            self._ge.driveline_frame, text="Eng Spd", bg="azure3", width=40
        )
        label.grid(row=2, column=3)

        eng_spd_entry = tk.Entry(
            self._ge.driveline_frame,
            textvariable=self._ge.eng_spd,
            font=("calibre", 10, "normal"),
        )
        eng_spd_entry.grid(row=2, column=5)

        self._ge.current_spd_label = tk.Entry(
            self._ge.driveline_frame, font=("calibre", 10, "normal")
        )
        self._ge.current_spd_label.grid(row=2, column=4)
        self._ge.current_spd_label.insert(0, "0")

        sub_btn = tk.Button(
            self._ge.driveline_frame,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.dv_eng_spd,
        )
        sub_btn.grid(row=2, column=6)

        label = tk.Label(
            self._ge.driveline_frame, text="chopper type", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.chopper_type_var,
            str("IC"),
            str("HHMC"),
            command=self.ui_call.chopper_type_callback,
        )
        label.grid(row=4, column=3)
        self._ge.chopper_type_var.set("HHMC")
        menu.grid(row=4, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="IC gear", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.IC_gear,
            str("Gear0"),
            str("Gear1"),
            command=self.ui_call.IC_gear_callback,
        )
        label.grid(row=5, column=3)
        self._ge.IC_gear.set("Gear1")
        menu.grid(row=5, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="HHMC gear", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.HHMC_gear,
            str("Gear0"),
            str("Gear1"),
            command=self.ui_call.HHMC_gear_callback,
        )
        label.grid(row=6, column=3)
        self._ge.HHMC_gear.set("Gear1")
        menu.grid(row=6, column=4)

        label = tk.Label(self._ge.driveline_frame, text="AuxPTO", bg="azure3", width=40)
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.Aux_PTO_enabled_str,
            str("disabled"),
            str("enabled"),
            command=self.ui_call.aux_callback,
        )
        label.grid(row=7, column=3)
        self._ge.Aux_PTO_enabled_str.set("disabled")
        menu.grid(row=7, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="feeder type", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.feeder_type,
            str("fixed"),
            str("variable"),
            command=self.ui_call.feeder_callback,
        )
        label.grid(row=8, column=3)
        self._ge.feeder_type.set("variable")
        menu.grid(row=8, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="unload rate", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.unload_rate,
            str("slow_unload"),
            str("fast_unload"),
            command=self.ui_call.unload_type_callback,
        )
        label.grid(row=9, column=3)
        self._ge.unload_rate.set("fast_unload")
        menu.grid(row=9, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="dfr gear", bg="azure3", width=40
        )
        menu = tk.OptionMenu(
            self._ge.driveline_frame,
            self._ge.rotor_gear_box_var,
            str("rotor_gear_0"),
            str("rotor_gear_1"),
            str("rotor_gear_2"),
            command=self.ui_call.rotor_gear_box_callback,
        )
        label.grid(row=10, column=3)
        self._ge.rotor_gear_box_var.set("rotor_gear_2")
        menu.grid(row=10, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="feedroll slip", bg="azure3", width=20
        )
        label.grid(row=11, column=3)
        w4 = tk.Scale(
            self._ge.driveline_frame,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.feed_roll_var,
        )
        w4.set(self._ge.feed_roll)
        w4.grid(row=11, column=4)
        b2 = tk.Button(
            self._ge.driveline_frame,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.frfr_callback,
        )
        b2.grid(row=11, column=5)

        # update from new code:
        label = tk.Label(
            self._ge.driveline_frame, text="PTO LSD", bg="azure3", width=20
        )
        label.grid(row=12, column=3)
        self._ge.pto_lsd_label = tk.Entry(
            self._ge.driveline_frame,
            textvariable=self._ge.PTO_LSD,
            font=("calibre", 10, "normal"),
        )
        self._ge.pto_lsd_label.grid(row=12, column=4)

        label = tk.Label(
            self._ge.driveline_frame, text="PTO LSD", bg="azure3", width=20
        )
        label.grid(row=13, column=3)
        self._ge.pto_hsd_label = tk.Entry(
            self._ge.driveline_frame,
            textvariable=self._ge.PTO_HSD,
            font=("calibre", 10, "normal"),
        )
        self._ge.pto_hsd_label.grid(row=13, column=4)
        label = tk.Label(
            self._ge.driveline_frame, text="Aux PTO Status", bg="azure3", width=20
        )
        label.grid(row=14, column=3)
        self._ge.Aux_PTO_enabled_label_str = tk.Entry(
            self._ge.driveline_frame,
            textvariable=self._ge.Aux_PTO_enabled_str,
            font=("calibre", 10, "normal"),
        )
        self._ge.Aux_PTO_enabled_label_str.grid(row=14, column=4)

    # UCM_1 Tab
    def generate_clrm_ui(self):
        # This will create a LabelFrame
        label_frame_clrm = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="CLRM")
        label_frame_clrm.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_clrm, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_clrm,
            text="clrm_enable",
            variable=self._ge.clrm_plant_enabled,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.clrm_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.clrm_plant_enabled.set(1)

        label = tk.Label(label_frame_clrm, text="clrm period", bg="azure3", width=20)
        label.grid(row=2, column=1)
        w1 = tk.Scale(
            label_frame_clrm,
            from_=0,
            to=500,
            orient=tk.HORIZONTAL,
            variable=self._ge.period_slide,
        )
        w1.set(self._ge.period)
        w1.grid(row=2, column=2)

        label = tk.Label(label_frame_clrm, text="clrm pulse", bg="azure3", width=20)
        label.grid(row=3, column=1)
        w2 = tk.Scale(
            label_frame_clrm,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.pulse_slide,
        )
        w2.set(self._ge.pulse)
        w2.grid(row=3, column=2)

        label = tk.Label(label_frame_clrm, text="clrm degree", bg="azure3", width=20)
        label.grid(row=4, column=1)
        w3 = tk.Scale(
            label_frame_clrm,
            from_=0,
            to=360,
            orient=tk.HORIZONTAL,
            variable=self._ge.degree_slide,
        )
        w3.set(self._ge.degree)
        w3.grid(row=4, column=2)

        b1 = tk.Button(
            label_frame_clrm,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.clrm_callback,
        )
        b1.grid(row=3, column=3)

        label = tk.Label(
            label_frame_clrm, text="Tail Sensor spd", bg="azure3", width=20
        )
        label.grid(row=6, column=1)
        self._ge.clrm_label = tk.Entry(label_frame_clrm, font=("calibre", 10, "normal"))
        self._ge.clrm_label.grid(row=6, column=2)
        self._ge.clrm_label.insert(0, "0")

    def generate_ui_hdhr(self):
        # This will create a LabelFrame
        label_frame_hdhr = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="HDHR")
        label_frame_hdhr.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_hdhr, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdhr,
            text="hdhr_enable",
            variable=self._ge.hdhr_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdhr_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.hdhr_enable_var.set(1)

        label = tk.Label(label_frame_hdhr, text="header type", bg="azure3", width=20)
        menu = tk.OptionMenu(
            label_frame_hdhr,
            self._ge.hdhr_type_var,
            str("NO_HEAD"),
            str("CORN"),
            str("GRAIN"),
            str("DRAPER_VARIFEED"),
            str("PICKUP"),
            str("OTHER"),
            str("FOLDING_CORN"),
            str("SPARE7"),
            str("DRAPER_WITH_FA"),
            str("SPARE9"),
            str("SPARE10"),
            str("SPARE11"),
            str("SPARE12"),
            str("VARIFEED"),
            str("SPARE14"),
            str("SPARE15"),
            str("SPARE16"),
            str("SPARE17"),
            str("DRAPER_WITHOUT_FA"),
            str("SPARE19"),
            str("SPARE20"),
            command=self.ui_call.hdhr_type_callback,
        )
        label.grid(row=2, column=1)
        self._ge.hdhr_type_var.set("DRAPER_VARIFEED")
        menu.grid(row=2, column=2)

        label = tk.Label(label_frame_hdhr, text="hdr typ volt", bg="azure3", width=20)
        label.grid(row=3, column=1)
        self._ge.hdhr_type_volt_label = tk.Entry(
            label_frame_hdhr, font=("calibre", 10, "normal")
        )
        self._ge.hdhr_type_volt_label.grid(row=3, column=2)
        self._ge.hdhr_type_volt_label.insert(0, "0")

        label = tk.Label(label_frame_hdhr, text="hdr ext1 volt", bg="azure3", width=20)
        label.grid(row=4, column=1)
        self._ge.hdhr_ext1_volt_label = tk.Entry(
            label_frame_hdhr, font=("calibre", 10, "normal")
        )
        self._ge.hdhr_ext1_volt_label.grid(row=4, column=2)
        self._ge.hdhr_ext1_volt_label.insert(0, "0")

        label = tk.Label(label_frame_hdhr, text="hdr ext2 volt", bg="azure3", width=20)
        label.grid(row=5, column=1)
        self._ge.hdhr_ext2_volt_label = tk.Entry(
            label_frame_hdhr, font=("calibre", 10, "normal")
        )
        self._ge.hdhr_ext2_volt_label.grid(row=5, column=2)
        self._ge.hdhr_ext2_volt_label.insert(0, "0")

    def generate_ui_hdfn(self):
        # This will create a LabelFrame
        label_frame_hdfn = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="HDFN")
        label_frame_hdfn.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_hdfn, text="hor enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="hor_enable",
            variable=self._ge.hdfn_hor_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.hdfn_hor_enable_var.set(1)

        label = tk.Label(label_frame_hdfn, text="ver enable", bg="azure3", width=20)
        label.grid(row=2, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="ver_enable",
            variable=self._ge.hdfn_ver_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=2, column=2)
        self._ge.hdfn_ver_enable_var.set(1)

        label = tk.Label(label_frame_hdfn, text="vari enable", bg="azure3", width=20)
        label.grid(row=3, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="vari_enable",
            variable=self._ge.hdfn_vari_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=3, column=2)
        self._ge.hdfn_vari_enable_var.set(1)

        label = tk.Label(label_frame_hdfn, text="hor install", bg="azure3", width=20)
        label.grid(row=1, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="hor_install",
            variable=self._ge.hdfn_hor_install_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=1, column=4)
        self._ge.hdfn_hor_install_var.set(1)

        label = tk.Label(label_frame_hdfn, text="ver install", bg="azure3", width=20)
        label.grid(row=2, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="ver_install",
            variable=self._ge.hdfn_ver_install_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=2, column=4)
        self._ge.hdfn_ver_install_var.set(1)

        label = tk.Label(label_frame_hdfn, text="vari install", bg="azure3", width=20)
        label.grid(row=3, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="vari_install",
            variable=self._ge.hdfn_vari_install_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=3, column=4)
        self._ge.hdfn_vari_install_var.set(1)

        label = tk.Label(label_frame_hdfn, text="reel up sol", bg="azure3", width=20)
        reel_up_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_sol_reel_up_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_sol_reel_up_var.set(0)
        label.grid(row=4, column=1)
        reel_up_entry.grid(row=4, column=2)

        label = tk.Label(label_frame_hdfn, text="reel down sol", bg="azure3", width=20)
        reel_down_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_sol_reel_down_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_sol_reel_down_var.set(0)
        label.grid(row=4, column=3)
        reel_down_entry.grid(row=4, column=4)

        label = tk.Label(label_frame_hdfn, text="reel fore sol", bg="azure3", width=20)
        reel_fore_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_sol_reel_fore_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_sol_reel_fore_var.set(0)
        label.grid(row=5, column=1)
        reel_fore_entry.grid(row=5, column=2)

        label = tk.Label(label_frame_hdfn, text="reel aft sol", bg="azure3", width=20)
        reel_aft_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_sol_reel_aft_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_sol_reel_aft_var.set(0)
        label.grid(row=5, column=3)
        reel_aft_entry.grid(row=5, column=4)

        label = tk.Label(label_frame_hdfn, text="swap 1", bg="azure3", width=20)
        swap_1_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_swap_1_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_swap_1_var.set(0)
        label.grid(row=6, column=1)
        swap_1_entry.grid(row=6, column=2)

        label = tk.Label(label_frame_hdfn, text="swap 2", bg="azure3", width=20)
        swap_2_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_swap_2_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_swap_2_var.set(0)
        label.grid(row=6, column=3)
        swap_2_entry.grid(row=6, column=4)

        label = tk.Label(label_frame_hdfn, text="swap 3", bg="azure3", width=20)
        swap_3_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_swap_3_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_swap_3_var.set(0)
        label.grid(row=7, column=1)
        swap_3_entry.grid(row=7, column=2)

        label = tk.Label(label_frame_hdfn, text="vari pos", bg="azure3", width=20)
        label.grid(row=7, column=3)
        self._ge.hdfn_vari_pos_label = tk.Entry(
            label_frame_hdfn, font=("calibre", 10, "normal")
        )
        self._ge.hdfn_vari_pos_label.grid(row=7, column=4)
        self._ge.hdfn_vari_pos_label.insert(0, "2500")

        label = tk.Label(label_frame_hdfn, text="hor pos", bg="azure3", width=20)
        label.grid(row=8, column=1)
        self._ge.hdfn_hor_pos_label = tk.Entry(
            label_frame_hdfn, font=("calibre", 10, "normal")
        )
        self._ge.hdfn_hor_pos_label.grid(row=8, column=2)
        self._ge.hdfn_hor_pos_label.insert(0, "2500")

        label = tk.Label(label_frame_hdfn, text="ver pos", bg="azure3", width=20)
        label.grid(row=8, column=3)
        self._ge.hdfn_ver_pos_label = tk.Entry(
            label_frame_hdfn, font=("calibre", 10, "normal")
        )
        self._ge.hdfn_ver_pos_label.grid(row=8, column=4)
        self._ge.hdfn_ver_pos_label.insert(0, "2500")

        label = tk.Label(label_frame_hdfn, text="reel enable", bg="azure3", width=20)
        label.grid(row=9, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="reel_enable",
            variable=self._ge.hdfn_reel_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=9, column=2)
        self._ge.hdfn_reel_enable_var.set(1)

        label = tk.Label(label_frame_hdfn, text="ffa enable", bg="azure3", width=20)
        label.grid(row=9, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="ffa_enable",
            variable=self._ge.hdfn_ffa_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=9, column=4)
        self._ge.hdfn_ffa_enable_var.set(1)

        label = tk.Label(label_frame_hdfn, text="reel sol", bg="azure3", width=20)
        reel_sol_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_reel_sol_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_reel_sol_var.set(0)
        label.grid(row=10, column=1)
        reel_sol_entry.grid(row=10, column=2)

        label = tk.Label(label_frame_hdfn, text="ffa sol fore", bg="azure3", width=20)
        ffa_sol_fore_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_ffa_sol_fore_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_ffa_sol_fore_var.set(0)
        label.grid(row=10, column=3)
        ffa_sol_fore_entry.grid(row=10, column=4)

        label = tk.Label(label_frame_hdfn, text="ffa install", bg="azure3", width=20)
        label.grid(row=11, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdfn,
            text="ffa_install",
            variable=self._ge.hdfn_ffa_install_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdfn_callback,
        )
        c1.grid(row=11, column=2)
        self._ge.hdfn_ffa_install_var.set(1)

        label = tk.Label(label_frame_hdfn, text="reel pulse", bg="azure3", width=20)
        reel_pulse_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_reel_pulse_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_reel_pulse_var.set(120)
        label.grid(row=11, column=3)
        reel_pulse_entry.grid(row=11, column=4)

        label = tk.Label(label_frame_hdfn, text="reel rpm", bg="azure3", width=20)
        label.grid(row=12, column=1)
        self._ge.hdfn_reel_spd_label = tk.Entry(
            label_frame_hdfn, font=("calibre", 10, "normal")
        )
        self._ge.hdfn_reel_spd_label.grid(row=12, column=2)
        self._ge.hdfn_reel_spd_label.insert(0, "2500")

        label = tk.Label(label_frame_hdfn, text="ffa rpm", bg="azure3", width=20)
        label.grid(row=12, column=3)
        self._ge.hdfn_ffa_spd_label = tk.Entry(
            label_frame_hdfn, font=("calibre", 10, "normal")
        )
        self._ge.hdfn_ffa_spd_label.grid(row=12, column=4)
        self._ge.hdfn_ffa_spd_label.insert(0, "2500")

        label = tk.Label(label_frame_hdfn, text="ffa sol aft", bg="azure3", width=20)
        ffa_sol_aft_entry = tk.Entry(
            label_frame_hdfn,
            textvariable=self._ge.hdfn_ffa_sol_aft_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.hdfn_ffa_sol_aft_var.set(0)
        label.grid(row=13, column=1)
        ffa_sol_aft_entry.grid(row=13, column=2)

        sub_btn = tk.Button(
            label_frame_hdfn,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.hdfn_callback,
        )
        sub_btn.grid(row=13, column=3)

    # Added from new code:
    def generate_ui_hdhc(self):
        label_frame_hdhc = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="HDHC")
        label_frame_hdhc.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_hdhc, text="Lift Pressure", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdhc,
            text="lift_prs_enable",
            variable=self._ge.hdhc_lift_prs_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdhc_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.hdhc_lift_prs_enable_var.set(1)

        label = tk.Label(label_frame_hdhc, text="Feeder Angle", bg="azure3", width=20)
        label.grid(row=1, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdhc,
            text="fdr_ang_enable",
            variable=self._ge.hdhc_frd_ang_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdhc_callback,
        )
        c1.grid(row=1, column=4)
        self._ge.hdhc_frd_ang_enable_var.set(1)

        label = tk.Label(
            label_frame_hdhc, text="Ground Height Sensors", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        c1 = tk.Checkbutton(
            label_frame_hdhc,
            text="gnd_ht_enable",
            variable=self._ge.hdhc_gnd_height_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdhc_callback,
        )
        c1.grid(row=2, column=2)
        self._ge.hdhc_gnd_height_enable_var.set(1)

        label = tk.Label(
            label_frame_hdhc, text="Lateral Float Sensors", bg="azure3", width=20
        )
        label.grid(row=2, column=3)
        c1 = tk.Checkbutton(
            label_frame_hdhc,
            text="lat_float_enable",
            variable=self._ge.hdhc_lat_float_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.hdhc_callback,
        )
        c1.grid(row=2, column=4)
        self._ge.hdhc_lat_float_enable_var.set(1)

        ############ JUST FOR TESTING THE POT VALUE AND COMPARE ###############

        label = tk.Label(
            label_frame_hdhc, text="center_lh_height_volt_pot", bg="azure3", width=20
        )
        label.grid(row=4, column=1)
        self._ge.hdhc_center_lh_height_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_center_lh_height_volt_pot_label.grid(row=4, column=2)
        self._ge.hdhc_center_lh_height_volt_pot_label.insert(
            0, self._ge.hdhc_center_lh_height_volt_pot
        )

        label = tk.Label(
            label_frame_hdhc, text="lh_height_tilt_volt_pot", bg="azure3", width=20
        )
        label.grid(row=5, column=1)
        self._ge.hdhc_lh_height_tilt_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_lh_height_tilt_volt_pot_label.grid(row=5, column=2)
        self._ge.hdhc_lh_height_tilt_volt_pot_label.insert(
            0, self._ge.hdhc_lh_height_tilt_volt_pot
        )

        label = tk.Label(
            label_frame_hdhc, text="lift_prs_volt_pot", bg="azure3", width=20
        )
        label.grid(row=6, column=1)
        self._ge.hdhc_lift_prs_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_lift_prs_volt_pot_label.grid(row=6, column=2)
        self._ge.hdhc_lift_prs_volt_pot_label.insert(0, self._ge.hdhc_skid_plate_range)

        label = tk.Label(
            label_frame_hdhc, text="feeder_angle_volt_pot", bg="azure3", width=20
        )
        label.grid(row=7, column=1)
        self._ge.hdhc_feeder_angle_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_feeder_angle_volt_pot_label.grid(row=7, column=2)
        self._ge.hdhc_feeder_angle_volt_pot_label.insert(
            0, self._ge.hdhc_skid_plate_range
        )

        label = tk.Label(
            label_frame_hdhc, text="center_rh_height_volt_pot", bg="azure3", width=20
        )
        label.grid(row=4, column=3)
        self._ge.hdhc_center_rh_height_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_center_rh_height_volt_pot_label.grid(row=4, column=4)
        self._ge.hdhc_center_rh_height_volt_pot_label.insert(
            0, self._ge.hdhc_center_rh_height_volt_pot
        )

        label = tk.Label(
            label_frame_hdhc, text="rh_height_tilt_volt_pot", bg="azure3", width=20
        )
        label.grid(row=5, column=3)
        self._ge.hdhc_rh_height_tilt_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_rh_height_tilt_volt_pot_label.grid(row=5, column=4)
        self._ge.hdhc_rh_height_tilt_volt_pot_label.insert(
            0, self._ge.hdhc_rh_height_tilt_volt_pot
        )

        label = tk.Label(
            label_frame_hdhc, text="lateral_position_volt_pot", bg="azure3", width=20
        )
        label.grid(row=6, column=3)
        self._ge.hdhc_lateral_position_volt_pot_label = tk.Entry(
            label_frame_hdhc, font=("calibre", 10, "normal")
        )
        self._ge.hdhc_lateral_position_volt_pot_label.grid(row=6, column=4)
        self._ge.hdhc_lateral_position_volt_pot_label.insert(
            0, self._ge.hdhc_lateral_position_volt_pot
        )

    def generate_ui_fffa(self):
        label_frame_fffa = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="FFFA")
        label_frame_fffa.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_fffa, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_fffa,
            text="fffa_enable",
            variable=self._ge.fffa_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.fffa_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.fffa_enable_var.set(1)

        label = tk.Label(label_frame_fffa, text="Blockage Mode", bg="azure3", width=20)
        label.grid(row=2, column=1)
        c1 = tk.Checkbutton(
            label_frame_fffa,
            text="enable_blockage_mode",
            variable=self._ge.fffa_block_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.fffa_callback,
        )
        c1.grid(row=2, column=2)
        self._ge.fffa_block_enable_var.set(1)

        label = tk.Label(
            label_frame_fffa, text="Min Position (mV)", bg="azure3", width=20
        )
        label.grid(row=3, column=1)

        w3 = tk.Scale(
            label_frame_fffa,
            from_=0,
            to=5000,
            resolution=1,
            orient=tk.HORIZONTAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.fffa_min_position_var,
        )
        w3.set(self._ge.fffa_min_position)
        w3.grid(row=3, column=2)

        self._ge.fffa_min_position_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_min_position_label.grid(row=3, column=3)
        self._ge.fffa_min_position_label.insert(0, self._ge.fffa_min_position)

        sub_btn = tk.Button(
            label_frame_fffa,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.fffa_callback,
        )
        sub_btn.grid(row=3, column=4)

        label = tk.Label(
            label_frame_fffa, text="Max Position (mV)", bg="azure3", width=20
        )
        label.grid(row=4, column=1)

        w3 = tk.Scale(
            label_frame_fffa,
            from_=0,
            to=5000,
            resolution=1,
            orient=tk.HORIZONTAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.fffa_max_position_var,
        )
        w3.set(self._ge.fffa_max_position)
        w3.grid(row=4, column=2)

        self._ge.fffa_max_position_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_max_position_label.grid(row=4, column=3)
        self._ge.fffa_max_position_label.insert(0, self._ge.fffa_max_position)

        sub_btn = tk.Button(
            label_frame_fffa,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.fffa_callback,
        )
        sub_btn.grid(row=4, column=4)

        label = tk.Label(
            label_frame_fffa, text="Travel Rate (mV)", bg="azure3", width=20
        )
        label.grid(row=5, column=1)

        w3 = tk.Scale(
            label_frame_fffa,
            from_=0,
            to=60,
            resolution=1,
            orient=tk.HORIZONTAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.fffa_travel_rate_var,
        )
        w3.set(self._ge.fffa_travel_rate)
        w3.grid(row=5, column=2)

        self._ge.fffa_travel_rate_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_travel_rate_label.grid(row=5, column=3)
        self._ge.fffa_travel_rate_label.insert(0, self._ge.fffa_travel_rate)

        sub_btn = tk.Button(
            label_frame_fffa,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.fffa_callback,
        )
        sub_btn.grid(row=5, column=4)

        label = tk.Label(label_frame_fffa, text="sol fore", bg="azure3", width=20)
        label.grid(row=6, column=1)
        self._ge.fffa_sol_fore_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_sol_fore_label.grid(row=6, column=2)
        self._ge.fffa_sol_fore_label.insert(0, self._ge.fffa_sol_fore)

        label = tk.Label(label_frame_fffa, text="sol aft", bg="azure3", width=20)
        label.grid(row=6, column=3)
        self._ge.fffa_sol_aft_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_sol_aft_label.grid(row=6, column=4)
        self._ge.fffa_sol_aft_label.insert(0, self._ge.fffa_sol_aft)

        label = tk.Label(label_frame_fffa, text="sol aft", bg="azure3", width=20)
        label.grid(row=7, column=1)
        self._ge.fffa_position_pot_label = tk.Entry(
            label_frame_fffa, font=("calibre", 10, "normal")
        )
        self._ge.fffa_position_pot_label.grid(row=7, column=2)
        self._ge.fffa_position_pot_label.insert(0, self._ge.fffa_position_pot)

    def generate_ui_gdst(self):
        label_frame_gdst = tk.LabelFrame(self._ge.plant_model_ucm4_frame, text="GDST")
        label_frame_gdst.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_gdst, text="Plant enable", bg="azure3", width=15)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_gdst,
            text="gdst_enable",
            variable=self._ge.gdst_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.gdst_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.gdst_enable_var.set(1)

        label = tk.Label(label_frame_gdst, text="Tracks Tension", bg="azure3", width=15)
        label.grid(row=2, columnspan=5, sticky="ew")

        label = tk.Label(
            label_frame_gdst, text="Tension Left Track", bg="azure3", width=15
        )
        label.grid(row=3, column=1)
        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=250,
            resolution=1,
            orient=tk.HORIZONTAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_left_track_var,
        )
        w3.set(self._ge.gdst_leftTensionInput)
        w3.grid(row=3, column=2)

        self._ge.gdst_left_track_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_left_track_label.grid(row=3, column=3)
        self._ge.gdst_left_track_label.insert(0, self._ge.gdst_leftTensionInput)

        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            width="15",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=3, column=4)

        label = tk.Label(
            label_frame_gdst, text="Tension Right Track", bg="azure3", width=15
        )
        label.grid(row=4, column=1)
        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=250,
            resolution=1,
            orient=tk.HORIZONTAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_right_track_var,
        )
        w3.set(self._ge.gdst_rightTensionInput)
        w3.grid(row=4, column=2)

        self._ge.gdst_right_track_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_right_track_label.grid(row=4, column=3)
        self._ge.gdst_right_track_label.insert(0, self._ge.gdst_rightTensionInput)

        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            width="15",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=4, column=4)

        label = tk.Label(label_frame_gdst, text="Suspension Height Tracks", bg="azure3")
        label.grid(row=5, columnspan=5, sticky="ew")

        label = tk.Label(label_frame_gdst, text="Left Front", bg="azure3", width=10)
        label.grid(row=6, column=1)
        label = tk.Label(label_frame_gdst, text="Left Rear", bg="azure3", width=10)
        label.grid(row=6, column=2)
        label = tk.Label(label_frame_gdst, text="Right Front", bg="azure3", width=10)
        label.grid(row=6, column=3)
        label = tk.Label(label_frame_gdst, text="Right Rear", bg="azure3", width=10)
        label.grid(row=6, column=4)

        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.VERTICAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_left_front_var,
        )
        w3.set(self._ge.gdst_leftFrontInput)
        w3.grid(row=7, column=1)

        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.VERTICAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_left_rear_var,
        )
        w3.set(self._ge.gdst_leftRearInput)
        w3.grid(row=7, column=2)

        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.VERTICAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_right_front_var,
        )
        w3.set(self._ge.gdst_rightFrontInput)
        w3.grid(row=7, column=3)

        w3 = tk.Scale(
            label_frame_gdst,
            from_=0,
            to=100,
            resolution=1,
            orient=tk.VERTICAL,
            font=("calibre", 8, "normal"),
            variable=self._ge.gdst_right_rear_var,
        )
        w3.set(self._ge.gdst_rightRearInput)
        w3.grid(row=7, column=4)

        self._ge.gdst_left_front_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=10
        )
        self._ge.gdst_left_front_label.grid(row=8, column=1)
        self._ge.gdst_left_front_label.insert(0, self._ge.gdst_leftFrontInput)
        self._ge.gdst_left_rear_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=10
        )
        self._ge.gdst_left_rear_label.grid(row=8, column=2)
        self._ge.gdst_left_rear_label.insert(0, self._ge.gdst_leftRearInput)
        self._ge.gdst_right_front_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=10
        )
        self._ge.gdst_right_front_label.grid(row=8, column=3)
        self._ge.gdst_right_front_label.insert(0, self._ge.gdst_rightFrontInput)
        self._ge.gdst_right_rear_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=10
        )
        self._ge.gdst_right_rear_label.grid(row=8, column=4)
        self._ge.gdst_right_rear_label.insert(0, self._ge.gdst_rightRearInput)

        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=9, column=1)
        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=9, column=2)
        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=9, column=3)
        sub_btn = tk.Button(
            label_frame_gdst,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdst_callback,
        )
        sub_btn.grid(row=9, column=4)

        ######################## JUST FOR TESTING THE POT VALUE AND COMPARE ##############################

        label = tk.Label(label_frame_gdst, text="RightRearDisp", bg="azure3", width=15)
        label.grid(row=10, column=1)
        self._ge.gdst_RightRearDisp_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_RightRearDisp_pot_label.grid(row=10, column=2)
        self._ge.gdst_RightRearDisp_pot_label.insert(0, self._ge.RightRearDisp_pot)

        label = tk.Label(label_frame_gdst, text="LeftRearDisp", bg="azure3", width=15)
        label.grid(row=11, column=1)
        self._ge.gdst_LeftRearDisp_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_LeftRearDisp_pot_label.grid(row=11, column=2)
        self._ge.gdst_LeftRearDisp_pot_label.insert(0, self._ge.LeftRearDisp_pot)

        label = tk.Label(label_frame_gdst, text="RightFrontDisp", bg="azure3", width=15)
        label.grid(row=12, column=1)
        self._ge.gdst_RightFrontDisp_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_RightFrontDisp_pot_label.grid(row=12, column=2)
        self._ge.gdst_RightFrontDisp_pot_label.insert(0, self._ge.RightFrontDisp_pot)

        label = tk.Label(label_frame_gdst, text="LeftFrontDisp", bg="azure3", width=15)
        label.grid(row=10, column=3)
        self._ge.gdst_LeftFrontDisp_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_LeftFrontDisp_pot_label.grid(row=10, column=4)
        self._ge.gdst_LeftFrontDisp_pot_label.insert(0, self._ge.LeftFrontDisp_pot)

        label = tk.Label(
            label_frame_gdst, text="LeftTensionPressure", bg="azure3", width=15
        )
        label.grid(row=11, column=3)
        self._ge.gdst_LeftTensionPressure_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_LeftTensionPressure_pot_label.grid(row=11, column=4)
        self._ge.gdst_LeftTensionPressure_pot_label.insert(
            0, self._ge.LeftTensionPressure_pot
        )

        label = tk.Label(
            label_frame_gdst, text="RightTensionPressure", bg="azure3", width=15
        )
        label.grid(row=12, column=3)
        self._ge.gdst_RightTensionPressure_pot_label = tk.Entry(
            label_frame_gdst, font=("calibre", 10, "normal"), width=15
        )
        self._ge.gdst_RightTensionPressure_pot_label.grid(row=12, column=4)
        self._ge.gdst_RightTensionPressure_pot_label.insert(
            0, self._ge.RightTensionPressure_pot
        )

    def generate_ui_agge(self):
        # This will create a LabelFrame
        label_frame_agge = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="AGGE")
        label_frame_agge.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_agge, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_agge,
            text="agge_enable",
            variable=self._ge.agge_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.agge_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.agge_enable_var.set(1)

        label = tk.Label(
            label_frame_agge, text="Steering Manual Override", bg="azure3", width=20
        )
        label.grid(row=2, column=1)

        self._ge.agge_steering_wheel_override = tk.Button(
            label_frame_agge,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
            command=self.ui_call.agge_steering_override,
        )
        self._ge.agge_steering_wheel_override.grid(row=2, column=2)

        label = tk.Label(
            label_frame_agge, text="Steering_W Motion Sensor", bg="azure3", width=20
        )
        label.grid(row=2, column=3)
        self._ge.agge_wheel_label = tk.Entry(
            label_frame_agge, font=("calibre", 10, "normal")
        )
        self._ge.agge_wheel_label.insert(0, 0)
        self._ge.agge_wheel_label.grid(row=2, column=4)

        label = tk.Label(
            label_frame_agge, text="Steering Wheel State", bg="azure3", width=20
        )
        label.grid(row=3, column=1)

        sub_btn = tk.Button(
            label_frame_agge,
            text="Left",
            fg="white",
            bg="Steel Blue",
            width=20,
            command=self.ui_call.agge_steering_left_callback,
        )
        sub_btn.grid(row=3, column=2)
        sub_btn = tk.Button(
            label_frame_agge,
            text="Center",
            fg="white",
            bg="Steel Blue",
            width=20,
            command=self.ui_call.agge_steering_center_callback,
        )
        sub_btn.grid(row=3, column=3)
        sub_btn = tk.Button(
            label_frame_agge,
            text="Right",
            fg="white",
            bg="Steel Blue",
            width=20,
            command=self.ui_call.agge_steering_right_callback,
        )
        sub_btn.grid(row=3, column=4)

        label = tk.Label(
            label_frame_agge, text="Rear Axle Angle", bg="azure3", width=20
        )
        label.grid(row=4, column=1)
        self._ge.agge_angle_label = tk.Entry(
            label_frame_agge, font=("calibre", 10, "normal")
        )
        self._ge.agge_angle_label.grid(row=4, column=2)
        self._ge.agge_angle_label.insert(0, "0")

        label = tk.Label(
            label_frame_agge, text="Right Steer Sol", bg="azure3", width=20
        )
        label.grid(row=5, column=1)
        self._ge.agge_right_steer_sol_label = tk.Entry(
            label_frame_agge, font=("calibre", 10, "normal")
        )
        self._ge.agge_right_steer_sol_label.grid(row=5, column=2)
        self._ge.agge_right_steer_sol_label.insert(0, "0")

        label = tk.Label(label_frame_agge, text="Left Steer Sol", bg="azure3", width=20)
        label.grid(row=5, column=3)
        self._ge.agge_left_steer_sol_label = tk.Entry(
            label_frame_agge, font=("calibre", 10, "normal")
        )
        self._ge.agge_left_steer_sol_label.grid(row=5, column=4)
        self._ge.agge_left_steer_sol_label.insert(0, "0")

    def generate_ui_rrts(self):
        # This will create a LabelFrame
        label_frame_rrts = tk.LabelFrame(self._ge.plant_model_ucm1_frame, text="RRTS")
        label_frame_rrts.pack(expand="yes", fill="both")
        label = tk.Label(label_frame_rrts, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_rrts,
            text="rrts_enable",
            variable=self._ge.rrts_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.rrts_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.rrts_enable_var.set(1)

        label = tk.Label(
            label_frame_rrts, text="Rocktrap Open Switch", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        self._ge.rrts_rocktrap_open_switch = tk.Button(
            label_frame_rrts,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
            command=self.ui_call.rrts_rocktrap_open_sw_callback,
        )
        self._ge.rrts_rocktrap_open_switch.grid(row=2, column=2)
        label = tk.Label(
            label_frame_rrts, text="Rocktrap Close Switch", bg="azure3", width=20
        )
        label.grid(row=2, column=3)
        self._ge.rrts_rocktrap_close_switch = tk.Button(
            label_frame_rrts,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
            command=self.ui_call.rrts_rocktrap_close_sw_callback,
        )
        self._ge.rrts_rocktrap_close_switch.grid(row=2, column=4)

        label = tk.Label(
            label_frame_rrts, text="Rocktrap Open Sol", bg="azure3", width=20
        )
        label.grid(row=3, column=1)
        self._ge.rrts_rocktrap_open_sol_label = tk.Entry(
            label_frame_rrts, font=("calibre", 10, "normal")
        )
        self._ge.rrts_rocktrap_open_sol_label.grid(row=3, column=2)
        self._ge.rrts_rocktrap_open_sol_label.insert(0, "0")
        label = tk.Label(
            label_frame_rrts, text="Rocktrap Close Sol", bg="azure3", width=20
        )
        label.grid(row=3, column=3)
        self._ge.rrts_rocktrap_close_sol_label = tk.Entry(
            label_frame_rrts, font=("calibre", 10, "normal")
        )
        self._ge.rrts_rocktrap_close_sol_label.grid(row=3, column=4)
        self._ge.rrts_rocktrap_close_sol_label.insert(0, "0")

    # UCM_2 Tab
    def generate_ghcv_ui(self):
        # This will create a LabelFrame
        label_frame_ghcv = tk.LabelFrame(self._ge.plant_model_ucm2_frame, text="GHCV")
        label_frame_ghcv.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_ghcv, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_ghcv,
            text="ghcv_enable",
            variable=self._ge.ghcv_plant_enabled,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghcv_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.ghcv_plant_enabled.set(1)

        label = tk.Label(label_frame_ghcv, text="open error", bg="azure3", width=20)
        label.grid(row=2, column=1)
        c2 = tk.Checkbutton(
            label_frame_ghcv,
            text="open_error",
            variable=self._ge.error_open,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghcv_callback,
        )
        c2.grid(row=2, column=2)
        self._ge.error_open.set(0)

        label = tk.Label(label_frame_ghcv, text="close error", bg="azure3", width=20)
        label.grid(row=3, column=1)
        c2 = tk.Checkbutton(
            label_frame_ghcv,
            text="close_error",
            variable=self._ge.error_close,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghcv_callback,
        )
        c2.grid(row=3, column=2)
        self._ge.error_close.set(0)

        label = tk.Label(label_frame_ghcv, text="Time to close", bg="azure3", width=20)
        label.grid(row=4, column=1)
        self._ge.ghcv_label_close = tk.Entry(
            label_frame_ghcv, font=("calibre", 10, "normal")
        )
        self._ge.ghcv_label_close.grid(row=4, column=2)
        self._ge.ghcv_label_close.insert(0, "0")

        label = tk.Label(label_frame_ghcv, text="Time to open", bg="azure3", width=20)
        label.grid(row=5, column=1)
        self._ge.ghcv_label_open = tk.Entry(
            label_frame_ghcv, font=("calibre", 10, "normal")
        )
        self._ge.ghcv_label_open.grid(row=5, column=2)
        self._ge.ghcv_label_open.insert(0, "0")

        # testing purpose only, can be removed later

        label = tk.Label(label_frame_ghcv, text="cover open sol", bg="azure3", width=20)
        cover_open_entry = tk.Entry(
            label_frame_ghcv,
            textvariable=self._ge.cover_open,
            font=("calibre", 10, "normal"),
        )
        self._ge.cover_open.set(0)
        sub_btn = tk.Button(
            label_frame_ghcv,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghcv_callback,
        )
        label.grid(row=6, column=1)
        cover_open_entry.grid(row=6, column=2)
        sub_btn.grid(row=6, column=3)

        label = tk.Label(
            label_frame_ghcv, text="cover close sol", bg="azure3", width=20
        )
        cover_close_entry = tk.Entry(
            label_frame_ghcv,
            textvariable=self._ge.cover_closed,
            font=("calibre", 10, "normal"),
        )
        self._ge.cover_closed.set(0)
        sub_btn = tk.Button(
            label_frame_ghcv,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghcv_callback,
        )
        label.grid(row=7, column=1)
        cover_close_entry.grid(row=7, column=2)
        sub_btn.grid(row=7, column=3)

        label = tk.Label(
            label_frame_ghcv, text="sensor cover open", bg="azure3", width=20
        )
        label.grid(row=8, column=1)
        self._ge.open_label = tk.Entry(label_frame_ghcv, font=("calibre", 10, "normal"))
        self._ge.open_label.grid(row=8, column=2)
        self._ge.open_label.insert(0, self._ge.cover_open_sensor)

        label = tk.Label(
            label_frame_ghcv, text="sensor cover close", bg="azure3", width=20
        )
        label.grid(row=9, column=1)
        self._ge.close_label = tk.Entry(
            label_frame_ghcv, font=("calibre", 10, "normal")
        )
        self._ge.close_label.grid(row=9, column=2)
        self._ge.close_label.insert(0, self._ge.cover_close_sensor)

    def generate_ui_rsch(self):
        label_frame_rsch = tk.LabelFrame(self._ge.plant_model_ucm2_frame, text="RSCH")
        label_frame_rsch.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_rsch, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_rsch,
            text="rsch_enable",
            variable=self._ge.chopper_plant_enabled,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.rsch_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.chopper_plant_enabled.set(1)

        label = tk.Label(label_frame_rsch, text="chopper type", bg="azure3", width=20)
        menu = tk.OptionMenu(
            label_frame_rsch,
            self._ge.rsch_type_select,
            str("IC"),
            str("HHMC"),
            command=self.ui_call.rsch_type_callback,
        )
        label.grid(row=2, column=1)
        self._ge.rsch_type_select.set("IC")
        menu.grid(row=2, column=2)

        label = tk.Label(label_frame_rsch, text="gear", bg="azure3", width=20)
        menu = tk.OptionMenu(
            label_frame_rsch,
            self._ge.gear,
            str("Gear0"),
            str("Gear1"),
            str("Gear2"),
            command=self.ui_call.rsch_gear_callback,
        )
        label.grid(row=3, column=1)
        self._ge.gear.set("Gear0")
        menu.grid(row=3, column=2)

        label = tk.Label(label_frame_rsch, text="crop_load", bg="azure3", width=20)
        label.grid(row=4, column=1)
        w1 = tk.Scale(
            label_frame_rsch,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.load,
        )
        w1.set(self._ge.crop_load_rsch)
        w1.grid(row=4, column=2)

        b1 = tk.Button(
            label_frame_rsch,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rsch_callback,
        )
        b1.grid(row=4, column=3)

        label = tk.Label(label_frame_rsch, text="Chopper spd", bg="azure3", width=20)
        label.grid(row=6, column=1)
        self._ge.rsch_label = tk.Entry(label_frame_rsch, font=("calibre", 10, "normal"))
        self._ge.rsch_label.grid(row=6, column=2)
        self._ge.rsch_label.insert(0, self._ge.rsch_spd)

    def generate_clfn_ui(self):
        # This will create a LabelFrame
        label_frame_clfn = tk.LabelFrame(self._ge.plant_model_ucm2_frame, text="CLFN")
        label_frame_clfn.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_clfn, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_clfn,
            text="clfn_enable",
            variable=self._ge.clfn_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.clfn_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.clfn_enable_var.set(1)

        label = tk.Label(label_frame_clfn, text="clfn sol drive", bg="azure3", width=20)
        clfn_sol_entry = tk.Entry(
            label_frame_clfn,
            textvariable=self._ge.clfn_pwm_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.clfn_pwm_var.set(0)
        sub_btn = tk.Button(
            label_frame_clfn,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.clfn_callback,
        )
        label.grid(row=2, column=1)
        clfn_sol_entry.grid(row=2, column=2)
        sub_btn.grid(row=2, column=3)

        label = tk.Label(label_frame_clfn, text="clfn RPM", bg="azure3", width=20)
        label.grid(row=3, column=1)
        self._ge.clfn_RPM_label = tk.Entry(
            label_frame_clfn, font=("calibre", 10, "normal")
        )
        self._ge.clfn_RPM_label.grid(row=3, column=2)
        self._ge.clfn_RPM_label.insert(0, "0")

    # UCM_3 Tab
    def generate_ui_ghts(self):
        # This will create a LabelFrame
        label_frame_ghts = tk.LabelFrame(self._ge.plant_model_ucm3_frame, text="GHTS")
        label_frame_ghts.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_ghts, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_ghts,
            text="ghts_enable",
            variable=self._ge.ghts_enabled_input,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghts_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.ghts_enabled_input.set(1)

        label = tk.Label(
            label_frame_ghts, text="Pos sensor enable", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        c1 = tk.Checkbutton(
            label_frame_ghts,
            text="pos_sensor",
            variable=self._ge.ghts_pos_sensor_enabled_input,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghts_callback,
        )
        c1.grid(row=2, column=2)
        self._ge.ghts_pos_sensor_enabled_input.set(1)

        label = tk.Label(
            label_frame_ghts, text="Cradle sensor enable", bg="azure3", width=20
        )
        label.grid(row=3, column=1)
        c1 = tk.Checkbutton(
            label_frame_ghts,
            text="cradle_sensor",
            variable=self._ge.ghts_cradle_sensor_enabled_input,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghts_callback,
        )
        c1.grid(row=3, column=2)
        self._ge.ghts_cradle_sensor_enabled_input.set(1)

        label = tk.Label(label_frame_ghts, text="Current", bg="azure3", width=20)
        label.grid(row=4, column=1)
        self._ge.ghts_label_current = tk.Entry(
            label_frame_ghts, font=("calibre", 10, "normal")
        )
        self._ge.ghts_label_current.grid(row=4, column=2)
        self._ge.ghts_label_current.insert(0, 0)

        label = tk.Label(label_frame_ghts, text="PWM", bg="azure3", width=20)
        label.grid(row=1, column=4)
        self._ge.ghts_label_pwm = tk.Entry(
            label_frame_ghts, font=("calibre", 10, "normal")
        )
        self._ge.ghts_label_pwm.grid(row=1, column=5)
        self._ge.ghts_label_pwm.insert(0, 0)

        label = tk.Label(label_frame_ghts, text="Position", bg="azure3", width=20)
        label.grid(row=2, column=4)
        self._ge.ghts_label_pos = tk.Entry(
            label_frame_ghts, font=("calibre", 10, "normal")
        )
        self._ge.ghts_label_pos.grid(row=2, column=5)
        self._ge.ghts_label_pos.insert(0, 0)

        label = tk.Label(label_frame_ghts, text="Position volt", bg="azure3", width=20)
        label.grid(row=3, column=4)
        self._ge.ghts_label_pos_volt = tk.Entry(
            label_frame_ghts, font=("calibre", 10, "normal")
        )
        self._ge.ghts_label_pos_volt.grid(row=3, column=5)
        self._ge.ghts_label_pos_volt.insert(0, 0)

        self._ge.cradle_button = tk.Button(
            label_frame_ghts,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
        )
        label = tk.Label(label_frame_ghts, text="Cradle sensor", bg="azure3", width=20)
        label.grid(row=4, column=4)
        self._ge.cradle_button.grid(row=4, column=5)

        label = tk.Label(label_frame_ghts, text="swing in sol", bg="azure3", width=20)
        swing_in_entry = tk.Entry(
            label_frame_ghts,
            textvariable=self._ge.ghts_input_solenoid,
            font=("calibre", 10, "normal"),
        )
        self._ge.ghts_input_solenoid.set(0)
        sub_btn = tk.Button(
            label_frame_ghts,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghts_callback,
        )
        label.grid(row=5, column=1)
        swing_in_entry.grid(row=5, column=2)
        sub_btn.grid(row=5, column=3)

        label = tk.Label(label_frame_ghts, text="swing out sol", bg="azure3", width=20)
        swing_in_entry = tk.Entry(
            label_frame_ghts,
            textvariable=self._ge.ghts_output_solenoid,
            font=("calibre", 10, "normal"),
        )
        self._ge.ghts_output_solenoid.set(0)
        sub_btn = tk.Button(
            label_frame_ghts,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghts_callback,
        )
        label.grid(row=5, column=4)
        swing_in_entry.grid(row=5, column=5)
        sub_btn.grid(row=5, column=6)

        label = tk.Label(label_frame_ghts, text="travel limiter", bg="azure3", width=20)
        label.grid(row=6, column=1)
        w3 = tk.Scale(
            label_frame_ghts,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.ghts_travel_limit,
        )
        w3.set(self._ge.ghts_travel_limiter)
        w3.grid(row=6, column=2)
        sub_btn = tk.Button(
            label_frame_ghts,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghts_callback,
        )
        sub_btn.grid(row=6, column=3)

    def generate_ui_rsck(self):
        # This will create a LabelFrame
        label_frame_rsck = tk.LabelFrame(self._ge.plant_model_ucm3_frame, text="RSCK")
        label_frame_rsck.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_rsck, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_rsck,
            text="rsck_enable",
            variable=self._ge.rsck_enabled_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.rsck_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.rsck_enabled_var.set(1)

        label = tk.Label(label_frame_rsck, text="IN Current(mA)", bg="azure3", width=20)
        label.grid(row=2, column=1)
        self._ge.rsck_label_in_current = tk.Entry(
            label_frame_rsck, font=("calibre", 10, "normal")
        )
        self._ge.rsck_label_in_current.grid(row=2, column=2)
        self._ge.rsck_label_in_current.insert(0, 0)

        label = tk.Label(
            label_frame_rsck, text="High speed Current(mA)", bg="azure3", width=20
        )
        label.grid(row=3, column=1)
        self._ge.rsck_label_high_speed_current = tk.Entry(
            label_frame_rsck, font=("calibre", 10, "normal")
        )
        self._ge.rsck_label_high_speed_current.grid(row=3, column=2)
        self._ge.rsck_label_high_speed_current.insert(0, 0)

        label = tk.Label(
            label_frame_rsck, text="OUT Current(mA)", bg="azure3", width=20
        )
        label.grid(row=2, column=4)
        self._ge.rsck_label_out_current = tk.Entry(
            label_frame_rsck, font=("calibre", 10, "normal")
        )
        self._ge.rsck_label_out_current.grid(row=2, column=5)
        self._ge.rsck_label_out_current.insert(0, 0)

        # ~ label = tk.Label(label_frame_rsck, text='High speed PWM', bg="azure3", width=20)
        # ~ label.grid(row=3, column=4)
        # ~ self._ge.rsck_label_high_speed_pwm = tk.Entry(label_frame_rsck, font=('calibre', 10, 'normal'))
        # ~ self._ge.rsck_label_high_speed_pwm.grid(row=3, column=5)
        # ~ self._ge.rsck_label_high_speed_pwm.insert(0, 0)

        label = tk.Label(label_frame_rsck, text="travel limiter", bg="azure3", width=20)
        label.grid(row=4, column=1)
        w3 = tk.Scale(
            label_frame_rsck,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.rsck_travel_limiter_var,
        )
        w3.set(self._ge.rsck_travel_limiter)
        w3.grid(row=4, column=2)
        sub_btn = tk.Button(
            label_frame_rsck,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rsck_callback,
        )
        sub_btn.grid(row=4, column=3)

        label = tk.Label(label_frame_rsck, text="high speed sol", bg="azure3", width=20)
        swing_in_entry = tk.Entry(
            label_frame_rsck,
            textvariable=self._ge.rsck_high_spd_sol_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.rsck_high_spd_sol_var.set(0)
        sub_btn = tk.Button(
            label_frame_rsck,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rsck_callback,
        )
        label.grid(row=4, column=4)
        swing_in_entry.grid(row=4, column=5)
        sub_btn.grid(row=4, column=6)

        label = tk.Label(label_frame_rsck, text="input sol", bg="azure3", width=20)
        swing_in_entry = tk.Entry(
            label_frame_rsck,
            textvariable=self._ge.rsck_in_sol_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.rsck_in_sol_var.set(0)
        sub_btn = tk.Button(
            label_frame_rsck,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rsck_callback,
        )
        label.grid(row=5, column=1)
        swing_in_entry.grid(row=5, column=2)
        sub_btn.grid(row=5, column=3)

        label = tk.Label(label_frame_rsck, text="output sol", bg="azure3", width=20)
        swing_in_entry = tk.Entry(
            label_frame_rsck,
            textvariable=self._ge.rsck_out_sol_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.rsck_out_sol_var.set(0)
        sub_btn = tk.Button(
            label_frame_rsck,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rsck_callback,
        )
        label.grid(row=5, column=4)
        swing_in_entry.grid(row=5, column=5)
        sub_btn.grid(row=5, column=6)

        label = tk.Label(label_frame_rsck, text="Position", bg="azure3", width=20)
        label.grid(row=6, column=1)
        self._ge.rsck_label_pos = tk.Entry(
            label_frame_rsck, font=("calibre", 10, "normal")
        )
        self._ge.rsck_label_pos.grid(row=6, column=2)
        self._ge.rsck_label_pos.insert(0, self._ge.rsck_pos)

        label = tk.Label(label_frame_rsck, text="sensor volt", bg="azure3", width=20)
        label.grid(row=6, column=4)
        self._ge.rsck_label_volt = tk.Entry(
            label_frame_rsck, font=("calibre", 10, "normal")
        )
        self._ge.rsck_label_volt.grid(row=6, column=5)
        self._ge.rsck_label_volt.insert(0, self._ge.rsck_volt)

    def generate_ui_ghps(self):
        # This will create a LabelFrame
        label_frame_ghps = tk.LabelFrame(
            self._ge.plant_model_ucm3_frame,
            text="GHPS",
        )
        label_frame_ghps.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_ghps, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_ghps,
            text="ghps_enable",
            variable=self._ge.ghps_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghps_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.ghps_enable_var.set(1)

        label = tk.Label(label_frame_ghps, text="Current", bg="azure3", width=20)
        label.grid(row=2, column=1)
        self._ge.ghps_curr_label = tk.Entry(
            label_frame_ghps, font=("calibre", 10, "normal")
        )
        self._ge.ghps_curr_label.grid(row=2, column=2)
        self._ge.ghps_curr_label.insert(0, 0)

        label = tk.Label(label_frame_ghps, text="PWM", bg="azure3", width=20)
        label.grid(row=2, column=4)
        self._ge.ghps_pwm_label = tk.Entry(
            label_frame_ghps, font=("calibre", 10, "normal")
        )
        self._ge.ghps_pwm_label.grid(row=2, column=5)
        self._ge.ghps_pwm_label.insert(0, 0)

        label = tk.Label(
            label_frame_ghps, text="h bridge current", bg="azure3", width=20
        )
        h_bridge_curr_entry = tk.Entry(
            label_frame_ghps,
            textvariable=self._ge.ghps_h_curr_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.ghps_h_curr_var.set(0)
        sub_btn = tk.Button(
            label_frame_ghps,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghps_callback,
        )
        label.grid(row=3, column=1)
        h_bridge_curr_entry.grid(row=3, column=2)
        sub_btn.grid(row=3, column=3)

        label = tk.Label(label_frame_ghps, text="h bridhe PWM", bg="azure3", width=20)
        h_bridge_pwm_entry = tk.Entry(
            label_frame_ghps,
            textvariable=self._ge.ghps_h_pwm_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.ghps_h_pwm_var.set(0)
        sub_btn = tk.Button(
            label_frame_ghps,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.ghps_callback,
        )
        label.grid(row=3, column=4)
        h_bridge_pwm_entry.grid(row=3, column=5)
        sub_btn.grid(row=3, column=6)

        label = tk.Label(label_frame_ghps, text="bridge enable", bg="azure3", width=20)
        label.grid(row=4, column=1)
        c2 = tk.Checkbutton(
            label_frame_ghps,
            text="bridge_enable",
            variable=self._ge.ghps_bridge_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.ghps_callback,
        )
        c2.grid(row=4, column=2)
        self._ge.ghps_bridge_enable_var.set(1)

        self._ge.ghps_bridge_button = tk.Button(
            label_frame_ghps,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
        )
        label = tk.Label(label_frame_ghps, text="bridge status", bg="azure3", width=20)
        label.grid(row=4, column=4)
        self._ge.ghps_bridge_button.grid(row=4, column=5)

        label = tk.Label(label_frame_ghps, text="Position", bg="azure3", width=20)
        label.grid(row=6, column=1)
        self._ge.ghps_pos_label = tk.Entry(
            label_frame_ghps, font=("calibre", 10, "normal")
        )
        self._ge.ghps_pos_label.grid(row=6, column=2)
        self._ge.ghps_pos_label.insert(0, self._ge.ghps_pos)

        label = tk.Label(label_frame_ghps, text="sensor volt", bg="azure3", width=20)
        label.grid(row=6, column=4)
        self._ge.ghps_pos_volt_label = tk.Entry(
            label_frame_ghps, font=("calibre", 10, "normal")
        )
        self._ge.ghps_pos_volt_label.grid(row=6, column=5)
        self._ge.ghps_pos_volt_label.insert(0, self._ge.ghps_pos_volt)

    def generate_ui_thcc(self):
        # This will create a LabelFrame
        label_frame_thcc = tk.LabelFrame(
            self._ge.plant_model_ucm3_frame,
            text="THCC",
        )
        label_frame_thcc.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_thcc, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_thcc,
            text="thcc_enable",
            variable=self._ge.thcc_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.thcc_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.thcc_enable_var.set(1)

        label = tk.Label(
            label_frame_thcc, text="Time Taken(seconds)", bg="azure3", width=20
        )
        label.grid(row=1, column=4)
        self._ge.thcc_time_taken_label = tk.Entry(
            label_frame_thcc, font=("calibre", 10, "normal")
        )
        self._ge.thcc_time_taken_label.grid(row=1, column=5)
        self._ge.thcc_time_taken_label.insert(0, self._ge.thcc_time_taken)

        label = tk.Label(label_frame_thcc, text="Position(mm)", bg="azure3", width=20)
        label.grid(row=2, column=1)
        self._ge.thcc_pos_label = tk.Entry(
            label_frame_thcc, font=("calibre", 10, "normal")
        )
        self._ge.thcc_pos_label.grid(row=2, column=2)
        self._ge.thcc_pos_label.insert(0, self._ge.thcc_pos)

        c1 = tk.Checkbutton(
            label_frame_thcc,
            text="pos_sensor_link",
            variable=self._ge.thcc_sensor_link_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.thcc_callback,
        )
        c1.grid(row=2, column=3)
        self._ge.thcc_sensor_link_var.set(1)

        label = tk.Label(label_frame_thcc, text="Sensor volt(V)", bg="azure3", width=20)
        label.grid(row=2, column=4)
        self._ge.thcc_pot_volt_label = tk.Entry(
            label_frame_thcc, font=("calibre", 10, "normal")
        )
        self._ge.thcc_pot_volt_label.grid(row=2, column=5)
        self._ge.thcc_pot_volt_label.insert(0, self._ge.thcc_pot_volt)

        label = tk.Label(
            label_frame_thcc, text="Breakaway Status", bg="azure3", width=20
        )
        label.grid(row=3, column=1)
        self._ge.thcc_breakaway_status = tk.Label(
            label_frame_thcc, text="Engaged", width=20
        )
        self._ge.thcc_breakaway_status.grid(row=3, column=2)
        self._ge.thcc_breakaway_button = tk.Button(
            label_frame_thcc,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Green",
            command=self.ui_call.thcc_breakaway,
        )
        self._ge.thcc_breakaway_button.grid(row=3, column=3)

    def generate_ui_gdpb(self):
        # This will create a LabelFrame
        label_frame_gdpb = tk.LabelFrame(
            self._ge.plant_model_ucm3_frame,
            text="GDPB",
        )
        label_frame_gdpb.pack(expand="yes", fill="both")
        label = tk.Label(label_frame_gdpb, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_gdpb,
            text="gdpb_enable",
            variable=self._ge.gdpb_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.gdpb_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.gdpb_enable_var.set(1)

        label = tk.Label(
            label_frame_gdpb, text="Park Brake Disengage Sol", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        self._ge.gdpb_disenage_sol_label = tk.Entry(
            label_frame_gdpb, font=("calibre", 10, "normal")
        )
        self._ge.gdpb_disenage_sol_label.grid(row=2, column=2)
        self._ge.gdpb_disenage_sol_label.insert(0, self._ge.gdpb_disenage_sol)

        c1 = tk.Checkbutton(
            label_frame_gdpb,
            text="Link to PB sol",
            variable=self._ge.gdpb_link_to_sensor_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.gdpb_callback,
        )
        c1.grid(row=3, column=5)
        self._ge.gdpb_link_to_sensor_var.set(1)

        label = tk.Label(
            label_frame_gdpb, text="Park Brake Sensor(V)", bg="azure3", width=20
        )
        label.grid(row=3, column=1)

        self._ge.gdpb_park_brake_sensor_label = tk.Entry(
            label_frame_gdpb, font=("calibre", 10, "normal")
        )
        self._ge.gdpb_park_brake_sensor_label.grid(row=3, column=2)
        self._ge.gdpb_park_brake_sensor_label.insert(0, self._ge.gdpb_park_brake_sensor)

        w3 = tk.Scale(
            label_frame_gdpb,
            from_=0,
            to=4.6,
            resolution=0.01,
            orient=tk.HORIZONTAL,
            variable=self._ge.gdpb_park_brake_sensor_var,
        )
        w3.set(self._ge.gdpb_park_brake_sensor)
        w3.grid(row=3, column=3)

        sub_btn = tk.Button(
            label_frame_gdpb,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdpb_callback,
        )
        sub_btn.grid(row=3, column=4)

    def generate_ui_gdhd(self):
        # This will create a LabelFrame
        label_frame_gdhd = tk.LabelFrame(
            self._ge.plant_model_ucm3_frame,
            text="GDHD",
        )
        label_frame_gdhd.pack(expand="yes", fill="both")
        label = tk.Label(label_frame_gdhd, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_gdhd,
            text="gdhd_enable",
            variable=self._ge.gdhd_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.gdhd_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.gdhd_enable_var.set(1)

        label = tk.Label(label_frame_gdhd, text="gear", bg="azure3", width=20)
        menu = tk.OptionMenu(
            label_frame_gdhd,
            self._ge.gear,
            str("Gear0"),
            str("Gear1"),
            str("Gear2"),
            command=self.ui_call.gdhd_gear_callback,
        )
        label.grid(row=1, column=4)
        self._ge.gear.set("Gear1")
        menu.grid(row=1, column=5)

        label = tk.Label(label_frame_gdhd, text="Rev Pump Sol", bg="azure3", width=20)
        label.grid(row=2, column=1)
        self._ge.gdhd_rev_sol_label = tk.Entry(
            label_frame_gdhd, font=("calibre", 10, "normal")
        )
        self._ge.gdhd_rev_sol_label.grid(row=2, column=2)
        self._ge.gdhd_rev_sol_label.insert(0, self._ge.gdhd_rev_sol)

        label = tk.Label(label_frame_gdhd, text="Fwd Pump Sol", bg="azure3", width=20)
        label.grid(row=2, column=4)
        self._ge.gdhd_fwd_sol_label = tk.Entry(
            label_frame_gdhd, font=("calibre", 10, "normal")
        )
        self._ge.gdhd_fwd_sol_label.grid(row=2, column=5)
        self._ge.gdhd_fwd_sol_label.insert(0, self._ge.gdhd_fwd_sol)

        label = tk.Label(
            label_frame_gdhd, text="Pump Displacement(cc)", bg="azure3", width=20
        )
        label.grid(row=3, column=1)
        pump_displace_entry = tk.Entry(
            label_frame_gdhd,
            textvariable=self._ge.gdhd_pump_displacement_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.gdhd_pump_displacement_var.set(self._ge.gdhd_max_pump_displacement)
        pump_displace_entry.grid(row=3, column=2)
        sub_btn = tk.Button(
            label_frame_gdhd,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdhd_callback,
        )
        sub_btn.grid(row=3, column=3)

        label = tk.Label(
            label_frame_gdhd, text="Motor Displacement(cc)", bg="azure3", width=20
        )
        label.grid(row=3, column=4)
        motor_displace_entry = tk.Entry(
            label_frame_gdhd,
            textvariable=self._ge.gdhd_motor_displacement_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.gdhd_motor_displacement_var.set(self._ge.gdhd_max_motor_displacement)
        motor_displace_entry.grid(row=3, column=5)

        sub_btn = tk.Button(
            label_frame_gdhd,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.gdhd_callback,
        )
        sub_btn.grid(row=3, column=6)

        label = tk.Label(
            label_frame_gdhd, text="Ground Speed(Pot Value)", bg="azure3", width=20
        )
        label.grid(row=4, column=1)
        self._ge.gdhd_ground_speed_label = tk.Entry(
            label_frame_gdhd, font=("calibre", 10, "normal")
        )
        self._ge.gdhd_ground_speed_label.grid(row=4, column=2)
        self._ge.gdhd_ground_speed_label.insert(0, self._ge.gdhd_ground_speed)

        label = tk.Label(
            label_frame_gdhd, text="Gear Speed(Pot Value)", bg="azure3", width=20
        )
        label.grid(row=4, column=4)
        self._ge.gdhd_gear_speed_label = tk.Entry(
            label_frame_gdhd, font=("calibre", 10, "normal")
        )
        self._ge.gdhd_gear_speed_label.grid(row=4, column=5)
        self._ge.gdhd_gear_speed_label.insert(0, self._ge.gdhd_gear_speed)

    def generate_ui_rssp(self):
        # This will create a LabelFrame
        label_frame_rssp = tk.LabelFrame(
            self._ge.plant_model_ucm3_frame,
            text="RSSP",
        )
        label_frame_rssp.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_rssp, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_rssp,
            text="rssp_enable",
            variable=self._ge.rssp_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.rssp_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.rssp_enable_var.set(1)

        label = tk.Label(label_frame_rssp, text="rssp right sol", bg="azure3", width=20)
        rssp_right_sol_entry = tk.Entry(
            label_frame_rssp,
            textvariable=self._ge.rssp_right_pwm_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.rssp_right_pwm_var.set(0)
        sub_btn = tk.Button(
            label_frame_rssp,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rssp_callback,
        )
        label.grid(row=2, column=1)
        rssp_right_sol_entry.grid(row=2, column=2)
        sub_btn.grid(row=2, column=3)

        label = tk.Label(label_frame_rssp, text="rssp left sol", bg="azure3", width=20)
        rssp_left_sol_entry = tk.Entry(
            label_frame_rssp,
            textvariable=self._ge.rssp_left_pwm_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.rssp_left_pwm_var.set(0)
        sub_btn = tk.Button(
            label_frame_rssp,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rssp_callback,
        )
        label.grid(row=3, column=1)
        rssp_left_sol_entry.grid(row=3, column=2)
        sub_btn.grid(row=3, column=3)

        label = tk.Label(
            label_frame_rssp, text="crop_load_right", bg="azure3", width=20
        )
        label.grid(row=4, column=1)
        w1 = tk.Scale(
            label_frame_rssp,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.crop_load_right_rssp_var,
        )
        w1.set(self._ge.crop_load_right_rssp)
        w1.grid(row=4, column=2)

        b1 = tk.Button(
            label_frame_rssp,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rssp_callback,
        )
        b1.grid(row=4, column=3)

        label = tk.Label(label_frame_rssp, text="crop_load_left", bg="azure3", width=20)
        label.grid(row=5, column=1)
        w1 = tk.Scale(
            label_frame_rssp,
            from_=0,
            to=100,
            orient=tk.HORIZONTAL,
            variable=self._ge.crop_load_left_rssp_var,
        )
        w1.set(self._ge.crop_load_left_rssp)
        w1.grid(row=5, column=2)

        b1 = tk.Button(
            label_frame_rssp,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.rssp_callback,
        )
        b1.grid(row=5, column=3)

        label = tk.Label(
            label_frame_rssp, text="spreader right RPM", bg="azure3", width=20
        )
        label.grid(row=2, column=4)
        self._ge.rssp_right_spd_label = tk.Entry(
            label_frame_rssp, font=("calibre", 10, "normal")
        )
        self._ge.rssp_right_spd_label.grid(row=2, column=5)
        self._ge.rssp_right_spd_label.insert(0, "0")

        label = tk.Label(
            label_frame_rssp, text="spreader left RPM", bg="azure3", width=20
        )
        label.grid(row=3, column=4)
        self._ge.rssp_left_spd_label = tk.Entry(
            label_frame_rssp, font=("calibre", 10, "normal")
        )
        self._ge.rssp_left_spd_label.grid(row=3, column=5)
        self._ge.rssp_left_spd_label.insert(0, "0")

        label = tk.Label(
            label_frame_rssp, text="spreader right curr", bg="azure3", width=20
        )
        label.grid(row=4, column=4)
        self._ge.rssp_right_curr_label = tk.Entry(
            label_frame_rssp, font=("calibre", 10, "normal")
        )
        self._ge.rssp_right_curr_label.grid(row=4, column=5)
        self._ge.rssp_right_curr_label.insert(0, "0")

        label = tk.Label(
            label_frame_rssp, text="spreader left curr", bg="azure3", width=20
        )
        label.grid(row=5, column=4)
        self._ge.rssp_left_curr_label = tk.Entry(
            label_frame_rssp, font=("calibre", 10, "normal")
        )
        self._ge.rssp_left_curr_label.grid(row=5, column=5)
        self._ge.rssp_left_curr_label.insert(0, "0")

    def generate_clfn_ui(self):
        # This will create a LabelFrame
        label_frame_clfn = tk.LabelFrame(self._ge.plant_model_ucm2_frame, text="CLFN")
        label_frame_clfn.pack(expand="yes", fill="both")

        label = tk.Label(label_frame_clfn, text="Plant enable", bg="azure3", width=20)
        label.grid(row=1, column=1)
        c1 = tk.Checkbutton(
            label_frame_clfn,
            text="clfn_enable",
            variable=self._ge.clfn_enable_var,
            onvalue=int(1),
            offvalue=int(0),
            command=self.ui_call.clfn_callback,
        )
        c1.grid(row=1, column=2)
        self._ge.clfn_enable_var.set(1)

        label = tk.Label(label_frame_clfn, text="clfn sol drive", bg="azure3", width=20)
        clfn_sol_entry = tk.Entry(
            label_frame_clfn,
            textvariable=self._ge.clfn_pwm_var,
            font=("calibre", 10, "normal"),
        )
        self._ge.clfn_pwm_var.set(0)
        sub_btn = tk.Button(
            label_frame_clfn,
            text="Update",
            fg="white",
            bg="Steel Blue",
            command=self.ui_call.clfn_callback,
        )
        label.grid(row=2, column=1)
        clfn_sol_entry.grid(row=2, column=2)
        sub_btn.grid(row=2, column=3)

        label = tk.Label(label_frame_clfn, text="clfn RPM", bg="azure3", width=20)
        label.grid(row=3, column=1)
        self._ge.clfn_RPM_label = tk.Entry(
            label_frame_clfn, font=("calibre", 10, "normal")
        )
        self._ge.clfn_RPM_label.grid(row=3, column=2)
        self._ge.clfn_RPM_label.insert(0, "0")

    # Settings Tab
    def generate_setting_ui(self):
        # Settings Container
        label_frame_setting = tk.LabelFrame(self._ge.setting_frame, text="Setting")
        label_frame_setting.pack(expand="yes", fill="both")

        # Key Status
        label = tk.Label(label_frame_setting, text="Key Status", bg="azure3", width=20)
        label.grid(row=1, column=1)
        self._ge.Key_Button = tk.Button(
            label_frame_setting,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Red",
            command=self.ui_call.key_callback,
        )
        self._ge.Key_Button.grid(row=1, column=2)

        # Battery Key
        label = tk.Label(
            label_frame_setting, text="Battery on Cmd", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        self._ge.Battery_Key_Button = tk.Button(
            label_frame_setting,
            height=1,
            width=4,
            bd=6,
            fg="Black",
            font=("Geneva", 6),
            bg="Red",
            command=self.ui_call.battery_key_callback,
        )
        self._ge.Battery_Key_Button.grid(row=2, column=2)

        # Debug Mode
        label_debug = tk.Label(
            label_frame_setting, text="Debug Mode", bg="azure3", width=20
        )
        label_debug.grid(row=3, column=1)
        self._ge.debug_mode_button = tk.Button(
            label_frame_setting,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Red",
            command=self.ui_call.debug_callback,
        )
        self._ge.debug_mode_button.grid(row=3, column=2)

        if self._ge.fei_compatible == 1:
            # CPU Usage
            label_cpu = tk.Label(
                label_frame_setting, text="CPU Usage", bg="azure3", width=20
            )
            label_cpu.grid(row=4, column=1)
            self._ge.cpu_entry = tk.Entry(
                label_frame_setting, bd=0, justify=CENTER, bg="#f0f0f0"
            )
            self._ge.cpu_entry.grid(row=4, column=2)

            # Simulator Mode Toggle
            label_sim = tk.Label(
                label_frame_setting, text="Simulator Mode", bg="azure3", width=20
            )
            label_sim.grid(row=5, column=1)
            self._ge.sim_button = tk.Button(
                label_frame_setting,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                command=self.ui_call.sim_callback,
            )
            self._ge.sim_button.grid(row=5, column=2)

            # Reset CAN button
            label_reset_can = tk.Label(
                label_frame_setting, text="Reset CAN Network", bg="azure3", width=20
            )
            label_reset_can.grid(row=6, column=1)
            self._ge.reset_can_button = tk.Button(
                label_frame_setting,
                height=1,
                width=4,
                bd=6,
                fg="black",
                font=("Geneva", 6),
                bg="skyblue",
                command=self.ui_call.reset_CAN,
            )
            # error, missing selection parameter     #error, missing selection parameter
            self._ge.reset_can_button.grid(row=6, column=2)

    # New CSS console
    def generate_cc_console_ui(self):
        label_frame_cc_console = tk.LabelFrame(
            self._ge.setting_frame, text="CSS Console"
        )
        label_frame_cc_console.pack(expand="yes", fill="both")

        # Thresher
        label = tk.Label(
            label_frame_cc_console, text="Thresher Engage", bg="azure3", width=20
        )
        label.grid(row=1, column=1)
        self._ge.thresher_engage_button = tk.Button(
            label_frame_cc_console,
            height=1,
            width=4,
            bd=6,
            bg="Red",
            fg="black",
            font=("Geneva", 6),
            command=self.ui_call.thresher_engage_callback,
        )
        self._ge.thresher_engage_button.grid(row=1, column=2)

        # Feeder
        label = tk.Label(
            label_frame_cc_console, text="Feeder Engage", bg="azure3", width=20
        )
        label.grid(row=2, column=1)
        self._ge.feeder_engage_button = tk.Button(
            label_frame_cc_console,
            height=1,
            width=4,
            bd=6,
            fg="black",
            font=("Geneva", 6),
            bg="Red",
            command=self.ui_call.feeder_engage_callback,
        )
        self._ge.feeder_engage_button.grid(row=2, column=2)
