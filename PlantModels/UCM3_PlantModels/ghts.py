# Comment out PWM Update_GUI Part
# May be add swing in and swing out current if need be
# self._gh_ghts_position_volt ot pot_val to self._gh.ghts_position angle 5 to 115
# self._gh_ghts_position_volt ot pot_val to voltage 1V to 4V


class ghts_plant:
    global _gh, _io
    prev_pos = 0
    flag = 0

    def __init__(self, ob1, ob2):
        self._gh = ob1
        self._io = ob2

    def volt_to_pot(self, pos):
        volt = -(
            (((pos - 1800) / 10) / 22.5) - 2.5
        )  # degree angle mentioned in eeprom converted to voltage
        pot_value = round(((volt) * 230) / 4.5)  # voltage converted to potmeter values
        return pot_value

    def calculate(self):
        if self.flag == 0:
            self.flag = 1

        if self._gh.ghts_enabled == 1:
            if self._gh.debug_mode == 0:
                self._gh.isswinginactive = self._io.data_read(624)
                self._gh.isswingoutactive = self._io.data_read(625)

            self._gh.swing_in_current = self._gh.isswinginactive * 1.2 / 5
            self._gh.swing_out_current = self._gh.isswingoutactive * 1.2 / 5

            # self._gh.ghts_pwm = self._gh.isswinginactive + self._gh.isswingoutactive

            if self._gh.ghts_pos_sensor_enabled == 1:
                if (
                    self._gh.isswinginactive != 0
                    and self._gh.swing_in_current > self._gh.g_curr_crack_in_ma_s32
                ):
                    if self._gh.ghts_position_volt <= self._gh.g_min_pos_volt_mv_s32:
                        self._gh.ghts_position_volt = self._gh.g_min_pos_volt_mv_s32
                        self._gh.ghts_input_solenoid.set(0)

                    else:
                        self._gh.ghts_position_volt -= 1 * (
                            self._gh.ghts_travel_limiter / 100
                        )
                        # ~ print("in :: ",self._gh.ghts_position_volt)

                elif (
                    self._gh.isswingoutactive != 0
                    and self._gh.swing_out_current > self._gh.g_curr_crack_out_ma_s32
                ):
                    if self._gh.ghts_position_volt >= self._gh.g_max_pos_volt_mv_s32:
                        self._gh.ghts_position_volt = self._gh.g_max_pos_volt_mv_s32
                        self._gh.ghts_output_solenoid.set(0)

                    else:
                        self._gh.ghts_position_volt += 1 * (
                            self._gh.ghts_travel_limiter / 100
                        )
                        # ~ print("out ::",self._gh.ghts_position_volt)

                self._gh.ghts_current = (
                    self._gh.swing_in_current + self._gh.swing_out_current
                )
                pot_val = self.volt_to_pot(self._gh.ghts_position_volt)
                self._gh.ghts_position = pot_val

            if self._gh.ghts_cradle_sensor_enabled == 1:
                # if  self._gh.ghts_position_volt < 1000:
                if self._gh.ghts_position >= 200:
                    self._gh.cradle_status = 1
                else:
                    self._gh.cradle_status = 0

            if self._gh.testing_active == 0:
                self._io.data_to_board(595, self._gh.ghts_position)  # tube position
                self._io.data_to_board(
                    513, (1 - self._gh.cradle_status)
                )  # cradle status
                # print(self._gh.ghts_position_volt,pot_val)


# ~ Below code is the actual code used before the above code was implemented
# ~ Uncomment the below code if above code is not used and commented
# ~ # changes made on 18052022 ghts

# ~ def calculate(self):
# ~ if self.flag == 0:
# ~ self._gh.g_min_pos_volt_mv_s32 = 7900
# ~ self.flag = 1

# ~ if self._gh.ghts_enabled == 1:
# ~ if self._gh.debug_mode == 0:
# ~ self._gh.isswinginactive = self._io.data_read(624)
# ~ self._gh.isswingoutactive = self._io.data_read(625)

# ~ self._gh.swing_in_current = self._gh.isswinginactive * 1.2/5
# ~ self._gh.swing_out_current = self._gh.isswingoutactive * 1.2/5

# ~ #self._gh.ghts_pwm = self._gh.isswinginactive + self._gh.isswingoutactive

# ~ if self._gh.ghts_pos_sensor_enabled == 1:
# ~ if self._gh.isswinginactive != 0 and self._gh.swing_in_current > self._gh.g_curr_crack_in_ma_s32:
# ~ if self._gh.ghts_position_volt >= self._gh.g_min_pos_volt_mv_s32:
# ~ self._gh.ghts_position_volt = self._gh.g_min_pos_volt_mv_s32
# ~ self._gh.ghts_input_solenoid.set(0)

# ~ else:
# ~ self._gh.ghts_position_volt += (12*(self._gh.ghts_travel_limiter / 100))

# ~ elif self._gh.isswingoutactive != 0 and self._gh.swing_out_current > self._gh.g_curr_crack_out_ma_s32:
# ~ if self._gh.ghts_position_volt <= self._gh.g_max_pos_volt_mv_s32:
# ~ self._gh.ghts_position_volt = self._gh.g_max_pos_volt_mv_s32
# ~ self._gh.ghts_output_solenoid.set(0)

# ~ else:
# ~ self._gh.ghts_position_volt -= (12*(self._gh.ghts_travel_limiter / 100))

# ~ self._gh.ghts_position = (self._gh.ghts_position_volt / 28.06) - 33.25
# ~ self._gh.ghts_current = self._gh.swing_in_current + self._gh.swing_out_current
# ~ self.prev_pos = self._gh.ghts_position
# ~ pot_val = round(((self._gh.ghts_position_volt /1000)*26))

# ~ if self._gh.ghts_cradle_sensor_enabled == 1:
# ~ #if  self._gh.ghts_position_volt < 1000:
# ~ if  pot_val == 205:
# ~ self._gh.cradle_status = 1
# ~ else:
# ~ self._gh.cradle_status = 0

# ~ if self._gh.testing_active == 0:
# ~ self._io.data_to_board(595, pot_val) #tube position
# ~ self._io.data_to_board(513, (1-self._gh.cradle_status)) #cradle status
# ~ #print(self._gh.ghts_position_volt,pot_val)
