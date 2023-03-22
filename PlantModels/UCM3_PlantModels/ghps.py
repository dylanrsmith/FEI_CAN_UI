class ghps_plant:
    global _ghps
    prev_pos = 0

    def __init__(self, ob):
        self._ghps = ob

    def pos_to_voltage(self, pos):
        """

        :param pos:
        :return:
        """
        volt = (pos + 750) * (2 / 3)
        return volt

    def voltage_to_pos(self, vol):
        """

        :param vol:
        :return:
        """
        pos = (vol * (3 / 2)) - 750
        return pos

    def calculate(self):
        if self._ghps.ghps_enable == 1:
            if self._ghps.ghps_bridge_enable == 1:
                self._ghps.ghps_curr = self._ghps.ghps_h_curr
                self._ghps.ghps_pwm = self._ghps.ghps_h_pwm
                if self._ghps.ghps_curr > 0:
                    if self._ghps.ghps_pos_volt >= self._ghps.ghps_max_volt:
                        self._ghps.ghps_pos_volt = self._ghps.ghps_max_volt
                    else:
                        self._ghps.ghps_pos_volt += self._ghps.ghps_tick_rate_pos
                elif self._ghps.ghps_curr < 0:
                    if self._ghps.ghps_pos_volt <= self._ghps.ghps_min_volt:
                        self._ghps.ghps_pos_volt = self._ghps.ghps_min_volt
                    else:
                        self._ghps.ghps_pos_volt -= self._ghps.ghps_tick_rate_pos
                self._ghps.ghps_pos = self.voltage_to_pos(self._ghps.ghps_pos_volt)
