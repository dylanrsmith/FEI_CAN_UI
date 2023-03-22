from lut import *


class rsch_plant:
    global _rs

    _lut = lut()

    ic_spd = [0, 620, 1210, 1800, 2390, 2980, 3580, 4160, 4750, 5820, 6880, 8230]
    ic_freq = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    beat_spd = [0, 360, 710, 1060, 1400, 1740, 2090, 2430, 2780, 3550, 4230, 5110]
    beat_freq = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    def __init__(self, ob1, ob2):
        self._rs = ob1
        self._io = ob2

    def ic_cal(self, spd):
        if spd == 0:
            return 200
        elif spd > 8230:
            return 100
        else:
            data = self._lut.get_val(self.ic_spd, self.ic_freq, spd)
            return data

    def beat_cal(self, spd):
        if spd == 0:
            return 200
        elif spd > 5110:
            return 100
        else:
            data = self._lut.get_val(self.beat_spd, self.beat_freq, spd)
            return data

    def hhmc_cal(self, spd):
        if spd < 620:
            return 200
        elif spd > 8230:
            return 100
        else:
            data = self._lut.get_val(self.ic_spd, self.ic_freq, spd)
            return data

    def calculate(self):
        if self._rs.rsch_enabled:
            if self._rs.Aux_PTO_enabled == 1:
                if self._rs.rsch_gear != 0:
                    if self._rs.rsch_type == self._rs.IC:
                        self._rs.rsch_spd = 800 if self._rs.rsch_gear == 1 else 3000
                    else:
                        self._rs.rsch_spd = 1000 if self._rs.rsch_gear == 1 else 4000
                    self._rs.rsch_spd = self._rs.rsch_spd * self._rs.current_spd / 1900
                    self._rs.rsch_spd = self._rs.rsch_spd * (
                        1 - (self._rs.crop_load_rsch / 100)
                    )
                else:
                    self._rs.rsch_spd = 0
            else:
                self._rs.rsch_spd = 0

    def rsch_temp(self):
        spn350 = 200
        spn351 = 200
        spn461 = 200
        #         print("chopper_type  ", self._rs.chopper_type)
        if self._rs.chopper_type == 0:  # IC
            spn461 = self.ic_cal(self._rs.sp_val[5])
            self._io.data_to_board(351, spn461)
            #             print("spn461  ", spn461)
            self._io.data_to_board(350, spn350)
        elif self._rs.chopper_type == 1:  # HHMC
            spn351 = self.beat_cal(self._rs.sp_val[13])
            spn350 = self.hhmc_cal(self._rs.sp_val[6])
            self._io.data_to_board(351, spn351)
            #             print("spn351  ", spn351)
            self._io.data_to_board(350, spn350)


#         print("spn350  ", spn350)
#         print("spn351  ", spn351)
#         print("spn461  ", spn461)
#         print("self._rs.sp_val[6]  ", self._rs.sp_val[6])
#         print("self._rs.sp_val[13]  ", self._rs.sp_val[13])
#         print("elf._rs.sp_val[5]  ", self._rs.sp_val[5])
