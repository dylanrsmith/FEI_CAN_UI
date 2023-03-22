import time
import threading
from Configuration.hashmap import *
from HwConnect.HwConnect import *
from JSON.Json_String import *
from eval_SPN_val import *

# ~ from startup_init import *  ## Add this if startup defautl is required while pytest are executed

Current_Key_State_1 = 0
Current_Key_State_2 = 0


class IOCtrl:
    global _gd
    data_buffer = []
    IOCtrl_dict = {}
    IOCtrl_dict_prev = {}
    I2C_buffer_1 = []
    I2C_buffer_2 = []
    I2C_buffer_3 = []
    I2C_add_list_read = [0x20, 0x21, 0x22, 0x23]
    I2C_add_list_write = [0x24, 0x25, 0x26, 0x27]
    StartTime = 0
    StopTime = 0
    HwConnect_obj = HwConnect()

    def __init__(self, ob):
        self._gd = ob
        self.eval_spn = SPN_value_conversion(self._gd)
        self.init_buffer()
        self.init_I2C_buffer()

    def init_buffer(self):
        # init buffer list and dict with 0 values at start only
        for i in range(1000):
            self.data_buffer.append(0)  # Update all buffers to zero
            self.IOCtrl_dict.update({i + 1: 0})
            self.IOCtrl_dict_prev.update({i + 1: 0})

    def init_I2C_buffer(self):
        # make the initial i2c data to 0
        self.I2C_buffer_1 = [0, 0, 0, 0]
        self.I2C_buffer_2 = [0, 0, 0, 0]
        self.I2C_buffer_3 = [0, 0, 0, 0]
        for i in range(0):
            for j in range(4):
                self.HwConnect_obj.writei2cbus2bytes_fn(
                    Racknr=(i + 1),
                    address=self.I2C_add_list_write[j],
                    value1=0,
                    value2=0,
                )

    # function to write data to IO board
    def data_to_board(self, SPN, val):
        """
        :param SPN:
        :param val:
        """
        # takes the data from python UI simulator and plant models
        if (
            self.IOCtrl_dict[SPN] != val
        ):  # only write data when data is not same as in buffer
            self.IOCtrl_dict[SPN] = val
            self.data_buffer[SPN] = val  # update the data buffer

    #     Not utilized at the moment
    #     highprio_spns = [347, 348]
    #
    #     def data_write_board_main(self):
    #         counter = 0
    #         for key in self.IOCtrl_dict:
    #             self.data_write_board(key)
    #             counter += 1
    #             if (counter == 20):
    #                 counter = 0
    #                 for k in self.highprio_spns:
    #                     self.data_write_board(k)

    def data_write_board(self, key):
        SPN = int(key)
        val = self.IOCtrl_dict[SPN]
        prev_val = self.IOCtrl_dict_prev[SPN]
        if val != prev_val:
            self.IOCtrl_dict_prev[SPN] = val
            type = self.eval_cmd(SPN)
            type = type.split(",")
            if int((type[0])[1:]) == 3:
                self.HwConnect_obj.writepotmeter_fn(
                    UCMnr=int((type[1])[1:]),
                    busnr=int((type[2])[1:]),
                    ic=int((type[3])[1:]),
                    potmeter=int((type[4])[1:-1]),
                    value=int(val),
                )
            elif int((type[0])[1:]) == 4:
                bit_pos = int((type[3])[1:])
                for j in range(4):
                    if int((type[2])[1:]) == self.I2C_add_list_write[j]:
                        addr_pos = j
                i = int((type[1])[1:])
                if i == 0:
                    data = self.I2C_buffer_1[addr_pos]
                elif i == 1:
                    data = self.I2C_buffer_2[addr_pos]
                else:
                    data = self.I2C_buffer_3[addr_pos]
                temp = pow(2, bit_pos)
                if (data & temp) == 0:
                    if val != 0:
                        final_data = data | temp
                        self.HwConnect_obj.writei2cbus2bytes_fn(
                            Racknr=int((type[1])[1:]),
                            address=int((type[2])[1:]),
                            value1=(final_data & 0x00FF),
                            value2=((final_data & 0xFF00) >> 8),
                        )
                        if i == 0:
                            self.I2C_buffer_1[addr_pos] = final_data
                        elif i == 1:
                            self.I2C_buffer_2[addr_pos] = final_data
                        else:
                            self.I2C_buffer_3[addr_pos] = final_data
                else:
                    if val == 0:
                        final_data = data - temp
                        self.HwConnect_obj.writei2cbus2bytes_fn(
                            Racknr=int((type[1])[1:]),
                            address=int((type[2])[1:]),
                            value1=(final_data & 0x00FF),
                            value2=((final_data & 0xFF00) >> 8),
                        )
                        if i == 0:
                            self.I2C_buffer_1[addr_pos] = final_data
                        elif i == 1:
                            self.I2C_buffer_2[addr_pos] = final_data
                        else:
                            self.I2C_buffer_3[addr_pos] = final_data

    # function to read data from IO board
    def data_from_board(
        self, SPN
    ):  # call from read thread and store in buffer. UI will read data from buffer
        """
        :param SPN:
        """
        # reads the requested data and store in that buffer
        type = self.eval_cmd(SPN)
        type = type.split(",")

        if int((type[0])[1:]) == 2:  # analog read
            val = self.HwConnect_obj.analogInput_fn(
                Racknr=int((type[1])[1:]),
                channel=int((type[2])[1:]),
                ADCnr=int((type[3])[1:]),
            )
            if val != self.IOCtrl_dict[SPN]:
                self.data_buffer[SPN] = val  # update the data buffer
                self.IOCtrl_dict[SPN] = val  # update the IO ctrl dict

        elif int((type[0])[1:]) == 1:  # i2c read
            bit_pos = int((type[3])[1:])
            read_val = self.HwConnect_obj.readi2cbus2bytes_fn(
                Racknr=int((type[1])[1:]), address=int((type[2])[1:])
            )
            temp = pow(2, bit_pos)

            if read_val & temp == 0:
                val = 0
            else:
                val = 1

            if val != self.IOCtrl_dict[SPN]:
                self.data_buffer[SPN] = val  # update the data buffer
                self.IOCtrl_dict[SPN] = val  # update the IO ctrl dict

    # in below 4 functions add logic to send back the error feedback to pytest
    def empty_string(self, id):
        print("the function is not available for SPN : ", id)

    def SPN_not_available(self, id):
        print("the selected SPN : ", id, " is not available")

    def unknown_command(self, id):
        print("the selected SPN : ", id, " has unknown command")

    def error_occured(self, id):
        print("error occured while reading SPN : ", id)

    def eval_cmd(self, SPN):
        """
        :param SPN:
        :return:
        """
        spn_number = "SPN" + str(SPN)
        return eval(spn_number)

    #         x = eval(spn_number)
    #         y = x
    #         return y

    # this function will be called from socket which will pass spn and val received from pytest via tcp/ip over ethernet
    def data_from_pytest_to_board(self, typ, SPN, val):
        """
        :param SPN:
        :param val:
        """
        if SPN == "key":
            if val == "on":
                if (
                    self._gd.Key_and_Battery_State == 2
                ):  ## Battery ON state then turn ON key and change the state to key active
                    self.Key_and_Battery_Write(Byte_1=4)  # Key ON
                    self._gd.Key_and_Battery_State = 3
                    time.sleep(2)
                if (
                    self._gd.Key_and_Battery_State == 1
                ):  ## Both OFF then Turn on Battery first change the state, then turn ON key and change the state
                    self.Key_and_Battery_Write(Byte_1=1)  # Battery ON
                    self._gd.Key_and_Battery_State = 2
                    time.sleep(2)
                    self.Key_and_Battery_Write(Byte_1=4)  # Key ON
                    self._gd.Key_and_Battery_State = 3
                    # ~ st = start_init(self._uc, self.io_ob)   ## Add this if startup defautl is required while pytest are executed
                    # ~ st.init_spn()                           ## Add this if startup defautl is required while pytest are executed
                    self.data_to_board(322, int(0))
                    time.sleep(0.5)
                    self.data_to_board(322, int(1))
                    time.sleep(0.5)
                    self.data_to_board(66, int(0))
                    time.sleep(0.5)
                    self.data_to_board(66, int(1))
            elif val == "off":
                if (
                    self._gd.Key_and_Battery_State == 3
                ):  ## Key ON then turn Both OFF and make change the state
                    self.Key_and_Battery_Write(Byte_1=5)  # Battery & Key both OFF
                    self._gd.Key_and_Battery_State = 1
        else:
            val = self.eval_spn.convert_value(SPN, val)
            print("SPN :: ", SPN, ", ", "Val :: ", val)
            self.data_to_board(SPN=SPN, val=val)

    def data_to_pytest_from_board(self, SPN):
        """
        :param SPN:
        :return:
        """
        cmd = "getio"
        type = self._gd.type_dict[SPN]
        spn = SPN
        val1 = self.data_read(SPN=SPN)
        val2 = 0
        val3 = 0
        json_class = UcmJsonClass(
            cmd=cmd, typ=type, spn=spn, val1=val1, val2=val2, val3=val3
        )
        msg = str.encode(json_class.to_json())
        return msg

    def key_switch(self, state):
        """
        :param state:
        """
        global Current_Key_State_1
        global Current_Key_State_2

        Current_Key_State_1 = state & 0x00FF
        Current_Key_State_2 = (state & 0xFF00) >> 8

        print(" Inside Key Function")
        print(" Key State : \t", state)
        print(" Current_Key_State_1 : \t", Current_Key_State_1)
        print(" Current_Key_State_2 : \t", Current_Key_State_2)
        print("\n")

        self.HwConnect_obj.writei2cbus2bytes_fn(
            Racknr=1,
            address=0x27,
            value1=Current_Key_State_1,
            value2=Current_Key_State_2,
        )

        # self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=1, address=0x27, value1=(state & 0x00FF), value2=((state & 0xFF00) >> 8))

    def battery_key_switch(self, state):
        """
        :param state:
        """
        global Current_Key_State_1
        global Current_Key_State_2

        state = state << 2
        Current_Key_State_1 = state & Current_Key_State_1
        Current_Key_State_2 = (state & Current_Key_State_1) >> 8

        print(" Inside Battery Function")
        print(" Battery State : \t", state)
        print(" Current_Key_State_1 : \t", Current_Key_State_1)
        print(" Current_Key_State_2 : \t", Current_Key_State_2)
        print("\n")

        self.HwConnect_obj.writei2cbus2bytes_fn(
            Racknr=1,
            address=0x27,
            value1=Current_Key_State_1,
            value2=Current_Key_State_2,
        )
        # self.HwConnect_obj.writei2cbus2bytes_fn(Racknr=1, address=0x27, value1=(state & 0x00FF), value2=((state & 0xFF00) >> 8))

    def Key_and_Battery_Init(self):
        self._gd.Key_and_Battery_State = 1
        self.HwConnect_obj.writei2cbus2bytes_fn(
            Racknr=1, address=0x27, value1=5, value2=0
        )

    def Key_and_Battery_Write(self, Byte_1):
        # print("Byte 1 :\t",Byte_1)
        self.HwConnect_obj.writei2cbus2bytes_fn(
            Racknr=1, address=0x27, value1=Byte_1, value2=0
        )

    def data_read(self, SPN):
        """
        :param SPN:
        :return:
        """
        return self.IOCtrl_dict[SPN]

    def scale_voltage(self, spn, val):
        """
        :param spn:
        :param val:
        :return:
        """
        max = self._gd.volt_scale_max_dict[spn]
        slope = (255 - 0) / max
        new_val = slope * val
        return new_val
