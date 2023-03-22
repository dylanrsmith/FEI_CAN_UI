from lut import *


class rssp_plant:
    global _rssp, _io
    _lut = lut()

    spreader_spd = [3, 108, 212, 317, 420, 524, 629, 733, 838]
    spreader_freq = [0, 10, 20, 30, 40, 50, 60, 70, 80]

    def __init__(self, ob1, ob2):
        self._rssp = ob1
        self._io = ob2

    def spreader_scale(self, spd):
        """
        :param spd:
        :return:
        """
        if spd < 3:
            return 200
        elif spd > 838:
            return 80
        else:
            data = self._lut.get_val(self.spreader_spd, self.spreader_freq, spd)
            return data

    def calculate_left_rpm(self):
        if self._rssp.debug_mode == 0:
            self._rssp.rssp_left_pwm = self._io.data_read(650)
        #             print("self._rssp.rssp_left_pwm  ", self._rssp.rssp_left_pwm)
        self._rssp.rssp_left_curr = self._rssp.rssp_left_pwm * 1.2
        self._rssp.rssp_left_spd = (
            (1 - (self._rssp.crop_load_left_rssp / 100)) * self._rssp.rssp_left_curr * 1
        )

    #        if self._rssp.rssp_left_spd >= 640:  # Uncomment this line and the line below to set an max limit to RPM
    #            self._rssp.rssp_left_spd = 640

    def calculate_right_rpm(self):
        if self._rssp.debug_mode == 0:
            self._rssp.rssp_right_pwm = self._io.data_read(651)
        #             print("self._rssp.rssp_right_pwm  ", self._rssp.rssp_right_pwm)
        self._rssp.rssp_right_curr = self._rssp.rssp_right_pwm * 1.2
        self._rssp.rssp_right_spd = (
            (1 - (self._rssp.crop_load_right_rssp / 100))
            * self._rssp.rssp_right_curr
            * 1
        )

    #        if self._rssp.rssp_right_spd >= 640:  # Uncomment this line and the line below to set an max limit to RPM
    #            self._rssp.rssp_right_spd = 640

    def write_speeds(self):
        if self._rssp.testing_active == 0:
            speed_left = self.spreader_scale(self._rssp.rssp_left_spd)
            speed_right = self.spreader_scale(self._rssp.rssp_right_spd)
            lh_spreader_on = self._io.data_read(676)
            rh_spreader_on = self._io.data_read(677)
            #             print("lh_spreader_on  ", lh_spreader_on)
            #             print("rh_spreader_on  ", rh_spreader_on)
            if lh_spreader_on == 0:
                speed_left = 200
            if rh_spreader_on == 0:
                speed_right = 200

            self._io.data_to_board(606, speed_left)
            self._io.data_to_board(607, speed_right)

    def calculate_rpm(self):
        if self._rssp.rssp_enable == 1:
            self.calculate_left_rpm()
            self.calculate_right_rpm()
            self.write_speeds()
