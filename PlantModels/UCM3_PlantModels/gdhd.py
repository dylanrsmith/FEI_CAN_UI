from lut import *


class gdhd_plant:
    global _gdhd
    _lut = lut()

    gnd_pot_freq = [0, 10, 50, 90]
    gnd_spd = [4, 85, 411, 842]

    gear_pot_freq = [0, 10, 50, 90]
    gear_spd = [12, 268, 1282, 2649]

    #### START 08032022 ####
    def __init__(self, ob1, ob2):
        self._gdhd = ob1
        self._io = ob2
        self.engine_to_pump_ratio = 67 / 44
        self.main_drive_shaft_teeth = 23
        self.main_differential_gear_teeth = 66
        self.input_shaftG1_drive_teeth = 23
        self.input_shaftG2_drive_teeth = 48
        self.gear1_teeth = 51
        self.gear2_teeth = 41
        self.gear_ratio_gear1 = self.input_shaftG1_drive_teeth / self.gear1_teeth
        self.differential_ratio = (
            self.main_drive_shaft_teeth / self.main_differential_gear_teeth
        )
        self.fwd_move_active = 0
        self.rev_move_active = 0
        self.gdhd_pump_flow_adc = 0
        self.timer_count = 0

    def gd_rpm_scale(self, spd, mode=0):
        if mode == 1:
            spd_table = self.gear_spd
            freq_table = self.gear_pot_freq
            min_spd = self.gear_spd[0]
            max_spd = self.gear_spd[3]
        else:
            spd_table = self.gnd_spd
            freq_table = self.gnd_pot_freq
            min_spd = self.gnd_spd[0]
            max_spd = self.gnd_spd[3]

        if spd < min_spd:
            return 200
        elif spd > max_spd:
            return 90
        else:
            data = self._lut.get_val(spd_table, freq_table, spd)
            return data

    def calculate(self):
        if self._gdhd.gdhd_enabled == 1:
            if self._gdhd.testing_active == 0:
                self._gdhd.gdhd_fwd_sol = self._io.data_read(638)  ## foward
                self._gdhd.gdhd_rev_sol = self._io.data_read(633)  ## reverse

            if self._gdhd.gdhd_fwd_sol > self._gdhd.gdhd_rev_sol:
                self.gdhd_pump_flow_adc = self._gdhd.gdhd_fwd_sol
            elif self._gdhd.gdhd_fwd_sol < self._gdhd.gdhd_rev_sol:
                self.gdhd_pump_flow_adc = self._gdhd.gdhd_rev_sol
            elif self._gdhd.gdhd_fwd_sol == 0 and self._gdhd.gdhd_rev_sol == 0:
                self.gdhd_pump_flow_adc = 0

            gdhd_pump_displacement = (
                self.gdhd_pump_flow_adc * self._gdhd.gdhd_max_pump_displacement
            ) / 720

            gdhd_pump_speed = self._gdhd.current_spd * self.engine_to_pump_ratio
            gdhd_pump_flow = gdhd_pump_speed * gdhd_pump_displacement

            # ~ gdhd_pump_flow = self._gdhd.current_spd * gdhd_pump_displacement
            gdhd_drive_motor = gdhd_pump_flow / self._gdhd.gdhd_max_motor_displacement

            if self._gdhd.gdhd_gear_state == 0:
                self.gdhd_gear_ratio = 0
            elif self._gdhd.gdhd_gear_state == 1:
                self.gdhd_gear_ratio = self.input_shaftG1_drive_teeth / self.gear1_teeth
            elif self._gdhd.gdhd_gear_state == 2:
                self.gdhd_gear_ratio = self.input_shaftG2_drive_teeth / self.gear2_teeth

            gdhd_gear1_rpm = gdhd_drive_motor * self.gear_ratio_gear1
            gdhd_ground_speed_rpm = (
                gdhd_drive_motor * self.gdhd_gear_ratio * self.differential_ratio
            )

            self.gdhd_ground_speed_pot = round(
                (self.gd_rpm_scale(gdhd_ground_speed_rpm)), 0
            )
            self.gdhd_gear_speed_pot = round((self.gd_rpm_scale(gdhd_gear1_rpm, 1)), 0)

            self._gdhd.gdhd_ground_speed = self.gdhd_ground_speed_pot
            self._gdhd.gdhd_gear_speed = self.gdhd_gear_speed_pot

            # ~ self.timer_count += 1
            # ~ if (self.timer_count >= 50):
            # ~ self.timer_count = 0
            # ~ print("-----------------------------------------------------------")
            # ~ print("ADC_conversion_cc :: ",gdhd_pump_displacement)
            # ~ print("Pump RPM ::",gdhd_pump_speed)
            # ~ print("pump flow :: ",gdhd_pump_flow)
            # ~ print("1st gear rpm :: ",gdhd_gear1_rpm)
            # ~ print("ground RPM :: ",gdhd_ground_speed_rpm)

            if self._gdhd.testing_active == 0:
                self._io.data_to_board(
                    604, self.gdhd_gear_speed_pot
                )  # SENSOR,RPM 1ST GEAR
                self._io.data_to_board(
                    603, self.gdhd_ground_speed_pot
                )  # SENSOR,RPM GROUND SPEED
