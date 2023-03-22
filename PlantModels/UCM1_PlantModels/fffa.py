class fffa_plant:
    def __init__(self, ob1, ob2):
        self._fa = ob1
        self._io = ob2

    def volt_to_pot(self, volt):
        pot_value = round((volt / 1000) * 240 / 4.656)
        return pot_value

    def calculate(self):
        if self._fa.fffa_enabled == 1:
            if self._fa.testing_active == 0:
                self._fa.fffa_sol_fore = self._io.data_read(115)
                self._fa.fffa_sol_aft = self._io.data_read(129)

            if self._fa.fffa_block_enabled != 1:
                self._fa.fffa_min_position = 4400
                self._fa.fffa_max_position = 500
                self._fa.fffa_travel_rate = 6

            if self._fa.fffa_sol_fore > 0 and self._fa.fffa_sol_aft <= 0:
                self._fa.fffa_position_volt -= self._fa.fffa_travel_rate
                if self._fa.fffa_position_volt < self._fa.fffa_min_position:
                    self._fa.fffa_position_volt = self._fa.fffa_min_position
            if self._fa.fffa_sol_aft > 0 and self._fa.fffa_sol_fore <= 0:
                self._fa.fffa_position_volt -= self._fa.fffa_travel_rate
                if self._fa.fffa_position_volt > self._fa.fffa_max_position:
                    self._fa.fffa_position_volt = self._fa.fffa_max_position

        pot_value = self.volt_to_pot(self._fa.fffa_position_volt)
        self._fa.fffa_position_pot = pot_value
        # if self._fa.testing_active == 0:
        #     self._fa.data_to_board(59, self.volt_to_pot(self._fa.fffa_position))
