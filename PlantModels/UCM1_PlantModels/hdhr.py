# ~ ##
# ~ hdhr_ext1_volt, hdhr_ext2_volt both digital output
# ~ 0 --> ON
# ~ 1 --> OFF
# ~ so reverse it before sending it to board
# ~ ##
class hdhr_plant:
    global _hdhr, _io

    def __init__(self, ob1, ob2):
        self._hdhr = ob1
        self._io = ob2
        # print("init")

    def volt_to_pot(self, volt):
        pot_value = round((volt / 1000) * 255 / 5)
        return pot_value

    def calculate_hdr_volt(self):
        if self._hdhr.hdhr_enable == 1:
            type = self._hdhr.hdhr_type

            if type == 0:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 0
            elif type == 1:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 4200
            elif type == 2:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 3300
            elif type == 3:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 2500
            elif type == 4:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 1700
            elif type == 5:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 800
            elif type == 6:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 4200
            elif type == 7:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 3300
            elif type == 8:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 2500
            elif type == 9:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 1700
            elif type == 10:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 1
                self._hdhr.hdhr_type_volt = 800
            elif type == 11:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 4200
            elif type == 12:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 3300
            elif type == 13:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 2500
            elif type == 14:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 1700
            elif type == 15:
                self._hdhr.hdhr_ext1_volt = 1
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 800
            elif type == 16:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 4200
            elif type == 17:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 3300
            elif type == 18:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 2500
            elif type == 19:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 1700
            elif type == 20:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 800
            else:
                self._hdhr.hdhr_ext1_volt = 0
                self._hdhr.hdhr_ext2_volt = 0
                self._hdhr.hdhr_type_volt = 0

            pot_value = self.volt_to_pot(self._hdhr.hdhr_type_volt)
            self._hdhr.hdhr_type_volt = pot_value

        # ~ if self._hdhr.testing_active == 0:
        # ~ self._io.data_to_board(55, 1-self._hdhr.hdhr_ext1_volt)
        # ~ self._io.data_to_board(56, 1-self._hdhr.hdhr_ext2_volt)
        # ~ self._io.data_to_board(79, pot_value)
