from lut import *


class clfn_plant:
    global _clfn, _io

    clfn_list_current = [
        0,
        600,
        700,
        800,
        900,
        1000,
        1100,
        1200,
        1300,
        1400,
        1500,
        2500,
    ]
    clfn_list_rpm = [
        0,
        316.026988,
        428.4011822,
        553.1259639,
        688.1017395,
        831.2289157,
        980.4078991,
        1133.539096,
        1288.522914,
        1443.259759,
        1595.650038,
        1595.650038,
    ]

    clfn_list_spd = [160, 310, 460, 610, 760, 920, 1070, 1230]
    clfn_list_freq = [10, 20, 30, 40, 50, 60, 70, 80]

    _lut = lut()

    def __init__(self, ob1, ob2):
        self._clfn = ob1
        self._io = ob2

    def RPM_to_freq(self, RPM):
        """

        :param RPM:
        :return:
        """
        freq = RPM
        return freq

    def clfn_io_scale(self, rpm):
        if rpm < 160:
            return 200
        elif rpm >= 1230:
            return 80
        else:
            spd = self._lut.get_val(self.clfn_list_spd, self.clfn_list_freq, rpm)
            return spd

    def calculate_RPM(self):
        if self._clfn.clfn_enable == 1:
            engine_spd = self._clfn.current_spd
            if self._clfn.testing_active == 0:
                self._clfn.clfn_pwm = self._io.data_read(385)
            self._clfn.clfn_curr = (self._clfn.clfn_pwm * 1.2 * 4.7) / 5.4
            hydro_RPM = self._lut.get_val(
                self.clfn_list_current, self.clfn_list_rpm, self._clfn.clfn_curr
            )
            if engine_spd > 0:
                RPM = hydro_RPM * 1900 / engine_spd
            else:
                RPM = 0
            freq = self.RPM_to_freq(RPM=RPM)
            if freq > 0:
                self._clfn.clfn_rpm = freq
            else:
                self._clfn.clfn_rpm = 0
            if self._clfn.clfn_rpm > 1230:
                self._clfn.clfn_rpm = 1230
            if self._clfn.testing_active == 0:
                temp = self.clfn_io_scale(self._clfn.clfn_rpm)
                self._io.data_to_board(352, temp)
