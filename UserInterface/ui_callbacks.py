from global_defines import *
from HwConnect.CAN_FEI import *
from PlantModels.Driveline import *
from startup_init import *
import time

key_battery_init_count = 0


class ui_callbacks:
    global _uc, _dv, io_ob, can2

    def __init__(self, ob1):
        """
        Initializes collection of UI callbacks.

        :param ob1: instance of global_defines
        :type ob1: Module
        :param ob2: Instance of IO_Ctrl
        :type ob2: Module
        """
        self._uc = ob1  # add dictionary to glcc

        self.can2 = CAN_FEI

    def buttonDig(self, i):
        """
        Callback for buttons contained within Digital I/P tab

        On click, will toggle state of linked Relay.

        :param i: Index of corresponding SPN
        :type i: int
        """
        sp = self._uc.dig_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.dig_state[sp] = 1 - self._uc.dig_state[sp]
        state = self._uc.dig_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def output_send(self, spn, selected_val):
        """
        Callback for dropdown menus (Output Boards)

        Will set Relay on Output Board to selected State.

        :param spn: SPN number
        :type spn: int
        :param selected_val: State to set Relay to:['Normal', 'Open-Circuit','Battery', 'Ground']
        :type selected_val: String
        """

        if selected_val != "Normal":
            # for selected_val in self._uc.all_widgets:
            #     selected_val.config(stat=tk.DISABLED)

            sp = spn
            state = selected_val
            brd_num = self._uc.board_dict[sp]
            rel_num = self._uc.channel_dict[sp]
            if state == "Normal":
                self.can2.flip_one(brd_num, rel_num, 0)
            elif state == "Open_Circuit":
                self.can2.flip_one(brd_num, rel_num, 1)
            elif state == "Ground":
                self.can2.flip_one(brd_num, rel_num, 2)
            elif state == "Battery":
                self.can2.flip_one(brd_num, rel_num, 3)

            time.sleep(5)

            for selected_val in self._uc.all_widgets:
                selected_val.config(stat=tk.NORMAL)

            indexOfSPN = self._uc.dig_ip_spn.index(spn)

            # Reset Option Menu Display Value
            if state == "Normal" or state == "Open_Circuit":
                self._uc.dig_ip_option_var[indexOfSPN].set("")

            if state == "Ground" or state == "Battery":
                self._uc.open_option_var[indexOfSPN].set("")

    def buttonVolt(self, i):
        new_data = self._uc.volt_string[i].get()
        sp = self._uc.vol_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def voltToggle(self, i):
        """
        Toggles state of Relays configured as Voltage Inputs.

        :param i: index of SPN to be toggled
        :type i: int
        """

        sp = self._uc.vol_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.volt_state[sp] = 1 - self._uc.volt_state[sp]
        state = self._uc.volt_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def dig_ip_callback(i, selection):
        """
        Updates Value of Digital Inputs and saves in Dictionary.

        'dig_ip_mode' dictionary updated with SPN : State

        :param i: SPN index
        :type i: int
        :param selection: 'Normal' or 'Open-Circuit'
        :type selection: String
        """
        selection = "self._uc." + selection
        selInt = int(eval(selection))
        _uc.dig_ip_mode.update({i: selInt})

        _uc.dig_ip_option[i] = tk.StringVar()

    def open_option_callback(self, i, selection):
        """
        Updates values of 'Open to' SPNS.

        Dictionary `open_mode` will be updated with specified SPN id and selected value. (open to ground or open to battery)

        :param i: Index of SPN
        :type i: int
        :param selection: "Ground" or "Battery"
        :type selection: String
        """
        selection = "self._uc" + selection
        self._uc.open_mode.update({i: selection})

    def open_button_callback(self):
        x = 1
        selection = "button"
        self._uc.open_option_callback(x, selection)

    def buttonPwmip(self, i):
        new_data = self._uc.pwm_ip_string[i].get()
        sp = self._uc.pwm_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def buttonFreq(self, i):
        new_data = self._uc.freq_string[i].get()
        sp = self._uc.fq_ip_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

    def buttonPulse(self, i):
        new_data = self._uc.pulse_string[i].get()
        sp = self._uc.pulse_spn[i]
        self.pass_to_board(spn_number=sp, data=new_data)
        self._uc.label_update = 1

        if self._uc.rrts_rocktrap_close_sw == 0:
            self._uc.rrts_rocktrap_close_sw = 1
        else:
            self._uc.rrts_rocktrap_close_sw = 0

    def voltToggle(self, i):
        """
        Toggles state of Relays configured as Voltage Inputs.
        :param i: index of SPN to be toggled
        :type i: int
        """

        sp = self._uc.vol_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.volt_state[sp] = 1 - self._uc.volt_state[sp]
        state = self._uc.volt_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def freqToggle(self, i):
        """
        Callback for toggling SPN's configured as Frequency Input.
        :param i: index of SPN to be toggled
        :type i: int
        """
        sp = self._uc.fq_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.freq_state[sp] = 1 - self._uc.freq_state[sp]
        state = self._uc.freq_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def pulseToggle(self, i):
        """
        Callback for toggling Relays configured as Pulse Input.
        :param i: index of SPN to be toggled.
        :type i: int
        """
        sp = self._uc.pulse_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.pulse_state[sp] = 1 - self._uc.pulse_state[sp]
        state = self._uc.pulse_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def pwmToggle(self, i):
        """
        Callback for toggling Relays configured as PWM input.
        :param i: SPN index
        :type i: int
        """
        sp = self._uc.pwm_ip_spn[i]
        brd_num = int(self._uc.board_dict[sp])
        rel_num = int(self._uc.channel_dict[sp])
        current_data = int(self._uc.UI_dict[sp])
        new_data = 1 - current_data
        self._uc.pwm_state[sp] = 1 - self._uc.pwm_state[sp]
        state = self._uc.pwm_state[sp]

        self.pass_to_board(spn_number=sp, data=new_data)
        self.can2.flip_one(brd_num, rel_num, state)

    def thresher_engage_callback(self):
        if self._uc.thresher_engage_state == 0:
            self._uc.thresher_engage_state = 1
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(322, int(0))
        else:
            self._uc.thresher_engage_state = 0
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(322, int(1))

    def feeder_engage_callback(self):
        if self._uc.feeder_engage_state == 0:
            self._uc.feeder_engage_state = 1
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(66, int(0))
        else:
            self._uc.feeder_engage_state = 0
            if self._uc.testing_active == 0:
                self.io_ob.data_to_board(66, int(1))

    def key_callback(self):
        current = self._uc.KeyIsON
        new = 1 - current
        self._uc.KeyIsON = new
        if self._uc.testing_active == 0:
            self.io_ob.key_switch(state=new)
        else:
            print(self._uc.KeyIsON)

    def battery_key_callback(self):
        # print("Battery Call Back")
        self.Key_and_Battery_Button(switch="Battery")

    def Key_and_Battery_Button(self, switch):
        if self._uc.Key_and_Battery_State == 3 and switch == "Key":
            self._uc.Key_and_Battery_State = 1

        if self._uc.Key_and_Battery_State == 1 and switch == "Battery":
            self._uc.Key_and_Battery_State = 2

        if self._uc.Key_and_Battery_State == 2 and switch == "Key":
            self._uc.Key_and_Battery_State = 3

        # print("Name of Button Pressed : \t",switch)
        # print("Key_and_Battery_State : \t", self._uc.Key_and_Battery_State)

        if self._uc.Key_and_Battery_State == 1:
            self.io_ob.Key_and_Battery_Write(Byte_1=5)
        if self._uc.Key_and_Battery_State == 2:
            self.io_ob.Key_and_Battery_Write(Byte_1=1)
        if self._uc.Key_and_Battery_State == 3:
            self.io_ob.Key_and_Battery_Write(Byte_1=4)
            if self._uc.testing_active == 0:
                # st = start_init(self._uc, self.io_ob)
                # st.init_spn()
                self.io_ob.data_to_board(322, int(0))
                time.sleep(0.5)
                self.io_ob.data_to_board(322, int(1))
                time.sleep(0.5)
                self.io_ob.data_to_board(66, int(0))
                time.sleep(0.5)
                self.io_ob.data_to_board(66, int(1))

    def debug_callback(self):
        current = self._uc.debug_mode
        new = 1 - current
        self._uc.debug_mode = new
        if self._uc.debug_mode == 0:
            self._uc.agge_enable = 0
            self._uc.hdfn_ffa_enable = 0
            self._uc.hdfn_hor_enable = 0
            self._uc.hdfn_ver_enable = 0
            self._uc.hdfn_vari_enable = 0
            self._uc.hdfn_reel_enable = 0
            self._uc.clrm_enabled = 0
            self._uc.hdhr_enable = 0
            self._uc.ghcv_enabled = 0
            self._uc.rsch_enabled = 0
            self._uc.clfn_enable = 0
            self._uc.ghts_enabled = 0
            self._uc.ghps_enable = 0
            self._uc.rsck_enabled = 0
            self._uc.thcc_enable = 0
            self._uc.rssp_enable = 0
        else:
            self._uc.agge_enable = 1
            self._uc.hdfn_ffa_enable = 1
            self._uc.hdfn_hor_enable = 1
            self._uc.hdfn_ver_enable = 1
            self._uc.hdfn_vari_enable = 1
            self._uc.hdfn_reel_enable = 1
            self._uc.clrm_enabled = 1
            self._uc.hdhr_enable = 1
            self._uc.ghcv_enabled = 1
            self._uc.rsch_enabled = 1
            self._uc.clfn_enable = 1
            self._uc.ghts_enabled = 1
            self._uc.ghps_enable = 1
            self._uc.rsck_enabled = 1
            self._uc.thcc_enable = 1
            self._uc.rssp_enable = 1

    def sim_callback(self):
        """
        Function to toggle the UI between simulator mode and normal mode.

        Greys out widgets when simulator mode is not active.

        Writes state of simMode to text file.
        """
        all_widgets = list(
            itertools.chain(
                self._uc.dig_ip_option,
                self._uc.open_option,
                self._uc.volt_toggle,
                self._uc.pwm_ip_toggle,
                self._uc.freq_toggle,
                self._uc.pulse_toggle,
                self._uc.actuator_load,
                self._uc.actuator_set,
                self._uc.actuator_pos,
                self._uc.actuator_btn,
            )
        )
        new = 1 - self._uc.SimMode
        self._uc.SimMode = new
        file = open("SimMode.txt", "w")
        a = str(self._uc.SimMode)
        file.write(a)
        file.close()

        if self._uc.SimMode == 1:
            self._uc.sim_button.config(bg="Green")
            for i in range(len(all_widgets)):
                try:
                    all_widgets[i].config(state=tk.NORMAL)
                except AttributeError:
                    pass
            # for i in range(80):
            #     self.can2.flip_all_off(i, i)

        elif self._uc.SimMode == 0:
            self._uc.sim_button.config(bg="Red")
            for i in range(len(all_widgets)):
                try:
                    all_widgets[i].config(state=tk.DISABLED)
                    if all_widgets[i].__class__.__name__ != "OptionMenu":
                        all_widgets[i].config(bg="azure3")
                except AttributeError:
                    pass
            for i in range(80):
                self.can2.flip_all_on(i, i)

    def reset_CAN(self):
        """
        When Button is clicked, this function will run a bash script to reset the CAN network.

        The script 'resetCAN.sh' sets the CAN bus down and back up.

        Baud Rate: 250,000
        """
        os.system("bash ./HwConnect/resetCAN.sh")

    def pass_to_board(self, spn_number, data):
        """
        Passes SPN number and index to terminal to be printed.

        {deprecated}
        """
        if self._uc.testing_active == 0:
            self.io_ob.data_to_board(SPN=spn_number, val=int(data))
        else:
            print("spn : ", spn_number)
            print("val : ", data)
