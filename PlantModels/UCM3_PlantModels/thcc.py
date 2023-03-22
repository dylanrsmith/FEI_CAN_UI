import time


class thcc_plant:
    global _thcc
    prev_pos = 0
    present_time = 0

    def __init__(self, ob1, ob2):
        self._thcc = ob1
        self._io = ob2
        self.link_flag = 1
        self.time_taken_pos = self._thcc.thcc_pos

    def pos_to_time(self, pos):
        pos_time = round(
            pos * (60 / 50)
        )  ## 60 is the seconds - time taken to complete 50mm distance
        return pos_time

    def pos_to_voltage(self, pos):
        volt = round(
            ((3.32 * pos) / 169), 2
        )  ## 169 is the max potmeter value, 3.32 is max voltage
        return volt

    def pos_to_pot_value(self, pos):
        pot_value = round(
            169 - (81 * (pos / 50))
        )  ## as the max voltage is equal to 0mm, the values are reversed and minused with 169.
        return pot_value  ## So 169 potmeter is 0mm and 81 potmeter is 50mm

    def calculate(self):
        if self._thcc.thcc_enable == 1:
            if self._thcc.testing_active == 0:
                self._thcc.thcc_concave_inc = self._io.data_read(713)  # open concave
                self._thcc.thcc_concave_dec = self._io.data_read(969)  # close concave

            if self._thcc.thcc_breakaway_state == 1:
                if self._thcc.testing_active == 0:
                    if (
                        self._thcc.thcc_concave_inc == 1
                        and self._thcc.thcc_concave_dec == 0
                    ):
                        if self._thcc.thcc_pos < 50.00:
                            if time.time() - self.present_time >= 1.2:
                                if self._thcc.thcc_sensor_link == 1:
                                    self._thcc.thcc_pos += 1
                                    if self.link_flag == 1:
                                        self.link_flag = 0
                                        self.time_taken_pos = self._thcc.thcc_pos - 1
                                else:
                                    self.link_flag = 1

                                if self.time_taken_pos < 50.00:
                                    self.time_taken_pos += 1
                                self.present_time = time.time()
                    elif (
                        self._thcc.thcc_concave_dec == 1
                        and self._thcc.thcc_concave_inc == 0
                    ):
                        if self._thcc.thcc_pos > 4.00:
                            if time.time() - self.present_time >= 1.2:
                                if self._thcc.thcc_sensor_link == 1:
                                    self._thcc.thcc_pos -= 1
                                    if self.link_flag == 1:
                                        self.link_flag = 0
                                        self.time_taken_pos = self._thcc.thcc_pos + 1
                                else:
                                    self.link_flag = 1

                                if self.time_taken_pos > 4.00:
                                    self.time_taken_pos -= 1
                                self.present_time = time.time()
                    self._thcc.thcc_pot = self.pos_to_pot_value(self._thcc.thcc_pos)
                    # ~ self._thcc.thcc_pot_volt = self.pos_to_voltage(self._thcc.thcc_pot)
                    self._thcc.thcc_time_taken = self.pos_to_time(self.time_taken_pos)
            else:
                self._thcc.thcc_pot = 88
                self._thcc.thcc_pos = 50

            self._thcc.thcc_pot_volt = self.pos_to_voltage(
                self._thcc.thcc_pot
            )  ## convert pot meter to voltage
            self._io.data_to_board(
                591, self._thcc.thcc_pot
            )  ## Concave position sensor SPN


#     def calculate(self):
#         self.rotor_type()
#         if self._thcc.thcc_enable == 1:
#             if self._thcc.thcc_bridge_enable == 2:
#                 self._thcc.thcc_curr = self._thcc.thcc_h_curr
#                 self._thcc.thcc_pwm = self._thcc.thcc_h_pwm
#                 #if self._thcc.thcc_curr > 0:
#                 #    if self._thcc.thcc_pos_volt >= self._thcc.thcc_max_volt:
#                 #        self._thcc.thcc_pos_volt = self._thcc.thcc_max_volt
#                 #    else:
#                 #        self._thcc.thcc_pos_volt += self._thcc.thcc_tick_rate_pos
#                 #elif self._thcc.thcc_curr < 0:
#                 #    if self._thcc.thcc_pos_volt <= self._thcc.thcc_min_volt:
#                 #        self._thcc.thcc_pos_volt = self._thcc.thcc_min_volt
#                 #    else:
#                 #        self._thcc.thcc_pos_volt -= self._thcc.thcc_tick_rate_pos
#                 #temp = self.voltage_to_pos(self._thcc.thcc_pos_volt)
#                 if  self._thcc.thcc_breakaway_state == 1:
#                     self._thcc.thcc_pos = self.pos_to_pot_value(self._thcc.thcc_set_pos)
#                     self._thcc.thcc_pos_volt = self.pos_to_voltage(self._thcc.thcc_pos)
#                 else:
#                     self._thcc.thcc_pos = 88
#
#                 self._thcc.thcc_pos_volt = self.pos_to_voltage(self._thcc.thcc_pos)
#                 self._io.data_to_board(591,self._thcc.thcc_pos)
