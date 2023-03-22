import time


class gdgs_plant:
    global _gdgs

    #### START 08032022 ####
    def __init__(self, ob1, ob2):
        self._gdgs = ob1
        self._io = ob2
        self.shift_in_motion = 0
        self.start_timer = 0
        self.prev_shift_state = 0

    def volt_to_pot(self, volt):
        volt = round(volt, 2)
        pot = round(((volt / 4.998) * 254), 0)
        return pot

    def calculate(self):
        if self._gdgs.gdgs_enabled == 1:
            if self._gdgs.testing_active == 0:
                self._gdgs.gdgs_gear_shift_inc = self._io.data_read(
                    714
                )  # 714 ##Shift gear increasing
                self._gdgs.gdgs_gear_shift_dec = self._io.data_read(
                    970
                )  # 970  ##Shift gear decreasing

            ####In this code when both trigger 1,####
            ####then value goes to max depending on inc or dec state ####


#             if self._gdgs.gdgs_link_to_elec_pos_sensor == 1:
#                 if self._gdgs.gdgs_gear_shift_inc == 1 and self._gdgs.gdgs_gear_shift_dec == 0:
#                     self.prev_shift_state = 1
#                     self._gdgs.gdgs_electric_shift_pos_sensor += 0.02
#                     if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.5:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 4.5
#
#                 elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 0:
#                     self.prev_shift_state = 2
#                     self._gdgs.gdgs_electric_shift_pos_sensor -= 0.02
#                     if self._gdgs.gdgs_electric_shift_pos_sensor <= 0.4:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 0.4
#                 elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 1:
#                     if self.prev_shift_state == 1:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 4.5
#                     elif self.prev_shift_state == 2:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 0.4
#                 else:
#                     self.prev_shift_state = 0

# ~ if self._gdgs.gdgs_link_to_elec_pos_sensor == 1:
# ~ if self._gdgs.gdgs_gear_shift_inc == 1 and self._gdgs.gdgs_gear_shift_dec == 0:
# ~ self._gdgs.gdgs_electric_shift_pos_sensor += 0.02
# ~ if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.5:
# ~ self._gdgs.gdgs_electric_shift_pos_sensor = 4.5

# ~ elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 0:
# ~ self._gdgs.gdgs_electric_shift_pos_sensor -= 0.02
# ~ if self._gdgs.gdgs_electric_shift_pos_sensor <= 0.4:
# ~ self._gdgs.gdgs_electric_shift_pos_sensor = 0.4

########### Trial Test Start (once inc then it will increase for given time period#######################
#             if self._gdgs.gdgs_link_to_elec_pos_sensor == 1:
#                 if self._gdgs.gdgs_gear_shift_inc == 1 and self._gdgs.gdgs_gear_shift_dec == 0 and self.shift_in_motion == 0:
#                     self.shift_in_motion = 1
#                     self.start_timer = time.time()
#                 elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 0 and self.shift_in_motion == 0:
#                     self.shift_in_motion = 2
#                     self.start_timer = time.time()
#                 elif (time.time() - self.start_timer >= 2) and (self.shift_in_motion == 1 or self.shift_in_motion == 2):
#                     self.shift_in_motion = 0
#
#                 if self._gdgs.gdgs_gear_shift_inc == 1 and self._gdgs.gdgs_gear_shift_dec == 0 and self.shift_in_motion == 1:
#                     if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.4:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.01
#                     elif self._gdgs.gdgs_electric_shift_pos_sensor >= 2.3 and self._gdgs.gdgs_electric_shift_pos_sensor < 2.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.01
#                     else:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.03
#                     if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.5:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 4.5
#
#                 elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 0 and self.shift_in_motion == 2:
#                     #self._gdgs.gdgs_electric_shift_pos_sensor -= 0.2
#                     if self._gdgs.gdgs_electric_shift_pos_sensor < 0.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.01
#                     elif self._gdgs.gdgs_electric_shift_pos_sensor >= 2.3 and self._gdgs.gdgs_electric_shift_pos_sensor < 2.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.01
#                     else:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.03
#
#                     if self._gdgs.gdgs_electric_shift_pos_sensor <= 0.4:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 0.4
#

################## Trial Test Ends ###########################


#             if self._gdgs.gdgs_link_to_elec_pos_sensor == 1:
#                 if self._gdgs.gdgs_gear_shift_inc == 1 and self._gdgs.gdgs_gear_shift_dec == 0:
#                     if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.3:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.005
#                     elif self._gdgs.gdgs_electric_shift_pos_sensor >= 2.3 and self._gdgs.gdgs_electric_shift_pos_sensor < 2.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.01
#                     else:
#                         self._gdgs.gdgs_electric_shift_pos_sensor += 0.04
#                     if self._gdgs.gdgs_electric_shift_pos_sensor >= 4.5:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 4.5
#
#                 elif self._gdgs.gdgs_gear_shift_dec == 1 and self._gdgs.gdgs_gear_shift_inc == 0:
#                     #self._gdgs.gdgs_electric_shift_pos_sensor -= 0.2
#                     if self._gdgs.gdgs_electric_shift_pos_sensor < 0.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.005
#                     elif self._gdgs.gdgs_electric_shift_pos_sensor >= 2.3 and self._gdgs.gdgs_electric_shift_pos_sensor < 2.6:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.01
#                     else:
#                         self._gdgs.gdgs_electric_shift_pos_sensor -= 0.04
#
#                     if self._gdgs.gdgs_electric_shift_pos_sensor <= 0.4:
#                         self._gdgs.gdgs_electric_shift_pos_sensor = 0.4

#                     if self._gdgs.testing_active == 0:
#                         self.volt_to_pot_value = self.volt_to_pot(self._gdgs.gdgs_electric_shift_pos_sensor)
#                         self._io.data_to_board(520, self.volt_to_pot_value


# ~ if self._gdgs.testing_active == 0:
# ~ self.volt_to_pot_value = self.volt_to_pot(self._gdgs.gdgs_electric_shift_pos_sensor)
# ~ self._io.data_to_board(520, self.volt_to_pot_value)
# ~ if self._gdgs.gdgs_gear_shift_inc == 1 or self._gdgs.gdgs_gear_shift_dec == 1:
# ~ self._gdgs.gdgs_electric_shift_pos_sensor = round(self._gdgs.gdgs_electric_shift_pos_sensor,3)
# ~ print("time,Pos Voltage,INC,DEC :: ",time.time(),self._gdgs.gdgs_electric_shift_pos_sensor,",",self._gdgs.gdgs_gear_shift_inc,",",self._gdgs.gdgs_gear_shift_dec)
