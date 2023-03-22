import time


class agge_plant:
    global _agge, _io

    def __init__(self, ob1, ob2):
        self._agge = ob1
        self._io = ob2
        self.start_movement = 0
        self.start_time = 0
        # print("init")

    def volt_to_pot(self, volt):
        pot_value = round(
            (volt / 1000) * 4.656 / 240
        )  ## check the potmeter value w.r.t to voltage
        return pot_value

    def calculate(self):
        if self._agge.agge_enable == 1:
            # ~ if self._agge.testing_active == 0:
            # ~ self._agge.agge_steer_right = self._io.data_read(128)
            # ~ self._agge.agge_steer_left = self._io.data_read(133)

            if self._agge.agge_steer_right == 0 and self._agge.agge_steer_left == 0:
                if self._agge.agge_steering_trigger == 1:
                    self.start_time = time.time()
                    self.start_movement = 1
                    self._agge.agge_steering_trigger = 0

                if self.start_movement == 1:
                    if (time.time() - self.start_time) >= 0.5:
                        if self._agge.agge_steering_state == 1:  ##Left
                            if self._agge.agge_angle <= 750:
                                self.start_movement = 0
                            else:
                                self._agge.agge_angle -= 175
                                self.start_time = time.time()
                        elif self._agge.agge_steering_state == 0:  ##center
                            if self._agge.agge_angle < 2500:
                                self._agge.agge_angle += 175
                                self.start_time = time.time()
                            elif self._agge.agge_angle > 2500:
                                self._agge.agge_angle -= 175
                                self.start_time = time.time()
                            else:
                                self.start_movement = 0
                        elif self._agge.agge_steering_state == 2:  ##right
                            if self._agge.agge_angle >= 4250:
                                self.start_movement = 0
                            else:
                                self._agge.agge_angle += 175
                                self.start_time = time.time()

                # ~ if self._agge.testing_active == 0:
                # ~ self._io.data_to_board(7, self.volt_to_pot(self._agge.agge_wheel))
                # ~ self._io.data_to_board(108, self.volt_to_pot(self._agge.agge_angle))

    # ~ def agge_pgn_callback(self):
    # ~ if self._agge.agge_calib_id == self._agge.WHEEL_CALIB:
    # ~ print("wheel calib")
    # ~ #todo as it is not implemented in c# code
    # ~ elif self._agge.agge_calib_id == self._agge.STEER_CALIB:
    # ~ if self._agge.agge_cid == self._agge.CALIB_NONE:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.NONE

    # ~ elif self._agge.agge_cid == self._agge.CALIB_COARSE_RIGHT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.COARSE_RIGHT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_COARSE_LEFT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.COARSE_LEFT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_FINE_RIGHT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.FINE_RIGHT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_FINE_LEFT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.FINE_LEFT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_TEST_RIGHT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.TEST_RIGHT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_TEST_LEFT:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.TEST_LEFT

    # ~ elif self._agge.agge_cid == self._agge.CALIB_DONE:
    # ~ self._agge.STEER_VALVE_STEP = self._agge.NONE

    # ~ def agge_calculate(self):
    # ~ if self._agge.agge_enable == 1:
    # ~ if self._agge.STEER_VALVE_STEP == self._agge.COARSE_RIGHT:
    # ~ if self._agge.agge_sol_right > 1100:
    # ~ self._agge.agge_angle += 20
    # ~ elif self._agge.STEER_VALVE_STEP == self._agge.COARSE_LEFT:
    # ~ if self._agge.agge_sol_left > 1100:
    # ~ self._agge.agge_angle -= 20
    # ~ elif self._agge.STEER_VALVE_STEP == self._agge.FINE_RIGHT:
    # ~ if self._agge.agge_sol_right > 800:
    # ~ self._agge.agge_angle += 5
    # ~ elif self._agge.STEER_VALVE_STEP == self._agge.FINE_LEFT:
    # ~ if self._agge.agge_sol_left > 800:
    # ~ self._agge.agge_angle -= 5

    # ~ if self._agge.agge_steer_wheel_enable == 1:
    # ~ if self._agge.agge_pulse < 4:
    # ~ self._agge.agge_wheel = 3500
    # ~ self._agge.agge_pulse += 1
    # ~ elif self._agge.agge_pulse < 6:
    # ~ self._agge.agge_wheel = 7000
    # ~ self._agge.agge_pulse = 0
    # ~ else:
    # ~ self._agge.agge_wheel = 3500
    # ~ self._agge.agge_pulse = 0

    # ~ def agge_plant_cal(self):
    # ~ self.agge_pgn_callback()
    # ~ self.agge_calculate()
