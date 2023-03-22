import pandas as pd
import os
import math
import datetime


# from HwConnect import *
# import the writepot meter and all functions from that file


class parse_excel:
    # predefined strings
    write_potmeter = "writepotmeter"
    write_i2cbus2bytes = "writei2cbus2bytes"
    input_variables = "inputvariables"
    adc_read = "adc_channel_read"
    Board_Number = "Board number"
    IC_Number = "IC number"
    Byte_value = "Byte value"

    op_list = [0, 0, 0, 0, 0]

    error_status = 0
    global df

    def __init__(self):
        #        path = os.path.dirname(__file__)
        #        path = path + "/ES-NG001-overview_subsystems_distributedarchitecture.xlsm"
        path = "ES-NG001-overview_subsystems_distributedarchitecture.xlsm"
        print("Path : ", path)
        self.df = pd.read_excel(path, "SPN", header=1)
        self.df = self.df.fillna("-1")
        # print(self.df)

    def calculate_bit_pos(self, data):
        """

        :param data:
        :return:
        """
        new_val = data[2:]  # scrap 0b
        byte_val = int(new_val, 2)
        for i in range(16):
            a = pow(2, i)
            if a == byte_val:
                bit_pos = i

        return bit_pos

    ##function call
    def execute_command(self, SPN_Number, value):
        """

        :param SPN_Number:
        :param value:
        :return:
        """
        self.error_status = 0
        # print("\n", SPN_Number)

        new_spn_Number = SPN_Number
        func_string = self.df.loc[new_spn_Number, "def function in Python"]
        # print("\n\n func string for ", SPN_Number, " is : ", func_string)

        stat = func_string == "-1"
        if stat == True:
            # print("string is NaN")
            str_6 = "[0, 0, 0, 0, 0]"
            return str_6

        if self.write_potmeter in func_string:
            self.op_list[0] = 3  # write identifier
            self.op_list[1] = self.df.loc[SPN_Number, "Rack Number"]  # Rack Number
            self.op_list[2] = self.df.loc[SPN_Number, "Bus Number"]  # bus no
            if self.Board_Number in func_string:
                self.op_list[3] = int(
                    self.df.loc[SPN_Number, "Board Number"]
                )  # bit pos

            elif self.IC_Number in func_string:
                self.op_list[3] = self.df.loc[SPN_Number, "IC Number"]  # bit pos

            self.op_list[4] = self.df.loc[
                SPN_Number, "Potmeter Number"
            ]  # potmeter Number

            return str(self.op_list)

        elif self.write_i2cbus2bytes in func_string:
            self.op_list[0] = 4  # write i2c identifier
            self.op_list[1] = self.df.loc[SPN_Number, "Rack Number"]  # Rack Number
            self.op_list[2] = int(self.df.loc[SPN_Number, "IC Address"], 16)  # ic addr
            temp = self.df.loc[SPN_Number, "Byte Value (to set)"]  # bit pos
            self.op_list[3] = self.calculate_bit_pos(data=str(temp))
            self.op_list[4] = 0

            return str(self.op_list)

        elif self.input_variables in func_string:
            self.op_list[0] = 1  # input variable identifier
            self.op_list[1] = self.df.loc[SPN_Number, "Rack Number"]  # Rack Number
            self.op_list[2] = int(self.df.loc[SPN_Number, "IC Address"], 16)  # ic addr
            self.op_list[3] = self.df.loc[
                SPN_Number, "Place in 16 bit answer [0..15]"
            ]  # bit pos
            self.op_list[4] = 0

            return str(self.op_list)

        elif self.adc_read in func_string:
            self.op_list[0] = 2  # adc identifier
            self.op_list[1] = self.df.loc[SPN_Number, "Rack Number"]  # Rack Number
            self.op_list[2] = self.df.loc[SPN_Number, "Channel"]  # Channel
            self.op_list[3] = self.df.loc[SPN_Number, "ADC nr"]  # adc Number
            self.op_list[4] = 0

            return str(self.op_list)

        else:
            str_5 = "[0, 0, 0, 0, 0]"
            #            print("empty")
            return str_5

    def error_handle(self, data):
        """

        :param data:
        :return:
        """
        stat = math.isnan(float(data))
        return stat

    def get_data(self, SPN_Number, column):
        """

        :param SPN_Number:
        :param column:
        :return:
        """
        data = self.df.loc[SPN_Number, column]
        stat = self.error_handle(data)
        return data, stat

    def spn_refactor(self, spn_data):
        """

        :param spn_data:
        :return:
        """
        spn = spn_data
        if 1 <= spn <= 352:
            pr = spn
        elif 354 <= spn <= 1037:
            pr = spn - 1
        elif 1792 <= spn <= 2047:
            pr = spn - 755

        return pr


# examples for test
pe = parse_excel()  # creat object

ct = datetime.datetime.now()

file_obj = open(r"hashmap.txt", "a+")
file_obj.close()

file_obj = open("hashmap.txt", "r+")
file_obj.truncate(0)
file_obj.close()

file_obj = open(r"hashmap.txt", "a+")
file_obj.write("#Hashmap file for NGC generated on : " + str(ct))

for i in range(1027):
    j = i + 1

    str_temp = pe.execute_command(j, 0)  # test for i2c
    str_spn = "SPN" + str(j)
    str_error = "error_occured"
    b = f'"{str_temp}"'
    c = f'"{str_error}"'
    try:
        file_obj.write("\n" + str_spn + " = " + b)
    except:
        file_obj.write("\n" + str_spn + " = " + c)

file_obj.close()

# if os.path.exists("hashmap.py"):
#    os.remove("hashmap.py")
# else:
#    print("The file does not exist")

path = os.path.dirname(__file__)
# old_path = path + "/hashmap.txt"
# new_path = path + "/hashmap.py"
old_path = "hashmap.txt"
new_path = "hashmap.py"
os.rename(old_path, new_path)
print("Hashmap file is updated")
