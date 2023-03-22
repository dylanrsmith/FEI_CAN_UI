class hdfn_plant:
    global _hdfn, _io

    def __init__(self, ob1, ob2):
        self._hdfn = ob1
        self._io = ob2
        # print("init")

    def volt_to_pot(self, volt):
        pot_value = round((volt / 1000) * 4.864 / 250)
        return pot_value

    def calculate_hor_pos(self):
        if self._hdfn.hdfn_hor_enable == 1:
            if self._hdfn.hdfn_hor_install == 1:
                if self._hdfn.testing_active == 0:
                    self._hdfn.hdfn_swap_1 = self._io.data_read(158)
                    self._hdfn.hdfn_swap_2 = self._io.data_read(159)
                    self._hdfn.hdfn_swap_3 = self._io.data_read(160)
                if (
                    self._hdfn.hdfn_swap_1 == 0
                    and self._hdfn.hdfn_swap_2 == 0
                    and self._hdfn.hdfn_swap_3 == 0
                ):
                    if self._hdfn.testing_active == 0:
                        self._hdfn.hdfn_sol_reel_fore = self._io.data_read(114)
                    if self._hdfn.hdfn_sol_reel_fore > 0:
                        if self._hdfn.hdfn_hor_pos <= self._hdfn.hdfn_min_voltage:
                            self._hdfn.hdfn_hor_pos = self._hdfn.hdfn_min_voltage
                        else:
                            self._hdfn.hdfn_hor_pos -= 5
                    if self._hdfn.testing_active == 0:
                        self._hdfn.hdfn_sol_reel_aft = self._io.data_read(130)
                    if self._hdfn.hdfn_sol_reel_aft > 0:
                        if self._hdfn.hdfn_hor_pos >= self._hdfn.hdfn_max_voltage:
                            self._hdfn.hdfn_hor_pos = self._hdfn.hdfn_max_voltage
                        else:
                            self._hdfn.hdfn_hor_pos += 5
            else:
                self._hdfn.hdfn_hor_pos = 0

    def calculate_ver_pos(self):
        if self._hdfn.hdfn_ver_enable == 1:
            if self._hdfn.hdfn_ver_install == 1:
                if (
                    self._hdfn.hdfn_swap_1 == 0
                    and self._hdfn.hdfn_swap_2 == 0
                    and self._hdfn.hdfn_swap_3 == 0
                ):
                    if self._hdfn.testing_active == 0:
                        self._hdfn.hdfn_sol_reel_down = self._io.data_read(113)
                    if self._hdfn.hdfn_sol_reel_down > 0:
                        if self._hdfn.hdfn_ver_pos <= self._hdfn.hdfn_min_voltage:
                            self._hdfn.hdfn_ver_pos = self._hdfn.hdfn_min_voltage
                        else:
                            self._hdfn.hdfn_ver_pos -= 5
                    if self._hdfn.testing_active == 0:
                        self._hdfn.hdfn_sol_reel_up = self._io.data_read(112)
                    if self._hdfn.hdfn_sol_reel_up > 0:
                        if self._hdfn.hdfn_ver_pos >= self._hdfn.hdfn_max_voltage:
                            self._hdfn.hdfn_ver_pos = self._hdfn.hdfn_max_voltage
                        else:
                            self._hdfn.hdfn_ver_pos += 5
            else:
                self._hdfn.hdfn_ver_pos = 0

    def calculate_vari_pos(self):
        if self._hdfn.hdfn_vari_enable == 1:
            if self._hdfn.hdfn_vari_install == 1:
                if self._hdfn.testing_active == 0:
                    self._hdfn.hdfn_swap_1 = self._io.data_read(158)
                    self._hdfn.hdfn_sol_reel_fore = self._io.data_read(114)
                if self._hdfn.hdfn_sol_reel_fore > 0 and self._hdfn.hdfn_swap_1 > 0:
                    if self._hdfn.hdfn_vari_pos <= self._hdfn.hdfn_min_voltage_vari:
                        self._hdfn.hdfn_vari_pos = self._hdfn.hdfn_min_voltage_vari
                    else:
                        self._hdfn.hdfn_vari_pos -= 5
                if self._hdfn.testing_active == 0:
                    self._hdfn.hdfn_swap_1 = self._io.data_read(158)
                    self._hdfn.hdfn_sol_reel_aft = self._io.data_read(130)
                if self._hdfn.hdfn_sol_reel_aft > 0 and self._hdfn.hdfn_swap_1 > 0:
                    if self._hdfn.hdfn_vari_pos >= self._hdfn.hdfn_max_voltage:
                        self._hdfn.hdfn_vari_pos = self._hdfn.hdfn_max_voltage
                    else:
                        self._hdfn.hdfn_vari_pos += 5

    def calculate_reel_spd(self):
        if self._hdfn.hdfn_reel_enable == 1:
            if self._hdfn.testing_active == 0:
                self._hdfn.hdfn_reel_sol = self._io.data_read(144)
            self._hdfn.hdfn_reel_curr = self._hdfn.hdfn_reel_sol * 12.5 / 5 / 10.0
            if self._hdfn.hdfn_reel_curr == 0:
                self._hdfn.hdfn_reel_spd = 0
            else:
                self._hdfn.hdfn_reel_spd_tmp = int(
                    (
                        (
                            pow(self._hdfn.hdfn_reel_curr, 3)
                            + pow(self._hdfn.hdfn_reel_curr, 2)
                            + self._hdfn.hdfn_reel_curr
                        )
                        * 10000
                        / 600
                    )
                    * self._hdfn.hdfn_reel_pulse
                    / 60
                )
                if self._hdfn.hdfn_reel_spd_tmp <= 0:
                    self._hdfn.hdfn_reel_spd = 0
                else:
                    self._hdfn.hdfn_reel_spd = self._hdfn.hdfn_reel_spd_tmp

    def calculate_ffa_spd(self):
        if self._hdfn.hdfn_ffa_enable == 1:
            if self._hdfn.hdfn_ffa_install == 1:
                if self._hdfn.testing_active == 0:
                    self._hdfn.hdfn_ffa_sol_aft = self._io.data_read(129)
                if self._hdfn.hdfn_ffa_sol_aft > 0:
                    if self._hdfn.hdfn_ffa_spd < self._hdfn.hdfn_ffa_min_volt:
                        self._hdfn.hdfn_ffa_spd = self._hdfn.hdfn_ffa_min_volt
                    else:
                        self._hdfn.hdfn_ffa_spd -= 5
                if self._hdfn.testing_active == 0:
                    self._hdfn.hdfn_ffa_sol_aft = self._io.data_read(115)
                if self._hdfn.hdfn_ffa_sol_fore > 0:
                    if self._hdfn.hdfn_ffa_spd > self._hdfn.hdfn_ffa_max_volt:
                        self._hdfn.hdfn_ffa_spd = self._hdfn.hdfn_ffa_max_volt
                    else:
                        self._hdfn.hdfn_ffa_spd += 5

    def write_to_board(self):
        if self._hdfn.testing_active == 0:
            self._io.data_to_board(83, self.volt_to_pot(self._hdfn.hdfn_hor_pos))
            self._io.data_to_board(84, self.volt_to_pot(self._hdfn.hdfn_ver_pos))
            self._io.data_to_board(209, self.volt_to_pot(self._hdfn.hdfn_vari_pos))
            self._io.data_to_board(93, self.volt_to_pot(self._hdfn.hdfn_reel_spd))
            # ~ self._io.data_to_board(59, self._hdfn.hdfn_ffa_spd)

    def calculate_hdr_pos(self):
        self.calculate_hor_pos()
        self.calculate_ver_pos()
        self.calculate_vari_pos()
        self.calculate_reel_spd()
        # ~ self.calculate_ffa_spd()
        self.write_to_board()
