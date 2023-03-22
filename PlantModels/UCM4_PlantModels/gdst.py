class gdst_plant:
    def __init__(self, ob1, ob2):
        self._gdst = ob1
        self._io = ob2
        self.susUpSpeed = 0.12
        self.susDownSpeed = -0.12
        self.min_distance_mm = 10
        self.max_distance_mm = 85
        self.LeftTensionPressure = 0
        self.RightTensionPressure = 0

        self.LeftFrontDisp = 0
        self.LeftRearDisp = 0
        self.RightFrontDisp = 0
        self.RightRearDisp = 0

    def AdjustWithMinMax(self, val, change, min, max):
        val += change
        if val > max:
            val = max
        if val < min:
            val = min

    def ConvertBarToMilliVoltage(self, prs_bar):
        volt = (0.5 + ((prs_bar / 250.0) * 4)) * 1000
        return volt

    def ConvertMmToMilliVoltage(self, mm):
        volt = (0.25 + ((mm / 95.0) * 4.5)) * 1000
        return volt

    def volt_to_pot(self, volt):
        pot_value = round((volt / 1000) * 255 / 4.9)
        return pot_value

    def calculate(self):
        if self._gdst.gdst_enabled == 1:
            if self._gdst.testing_active == 0:
                self._gdst.gdst_LeftShutOff = self._io.data_read(879)
                self._gdst.gdst_RightRearDown = self._io.data_read(880)
                self._gdst.gdst_RightRearUp = self._io.data_read(881)
                self._gdst.gdst_LeftRearUp = self._io.data_read(882)
                self._gdst.gdst_RightShutOff = self._io.data_read(885)
                self._gdst.gdst_TracksDischarge = self._io.data_read(886)
                self._gdst.gdst_LeftFrontDown = self._io.data_read(892)
                self._gdst.gdst_RightFrontUp = self._io.data_read(893)
                self._gdst.gdst_LeftRearDown = self._io.data_read(898)
                self._gdst.gdst_LeftFrontUp = self._io.data_read(899)
                self._gdst.gdst_RightFrontDown = self._io.data_read(900)

            #### Tension ####
            if self._gdst.gdst_TracksDischarge == 1:  ## Tensioning is possible
                if self._gdst.gdst_LeftShutOff == 1:
                    # Tensioning Left
                    self.AdjustWithMinMax(
                        self._gdst.gdst_leftTensionInput, 0.12, 0, 250
                    )
                if self._gdst.gdst_RightShutOff == 1:
                    # Tensioning Right
                    self.AdjustWithMinMax(
                        self._gdst.gdst_rightTensionInput, 0.12, 0, 250
                    )
            else:  # Untensioning is possible
                if self._gdst.gdst_LeftShutOff == 1:
                    # Untensioning left
                    self.AdjustWithMinMax(
                        self._gdst.gdst_leftTensionInput,
                        self.susUpSpeed,
                        self.min_distance_mm,
                        self.max_distance_mm,
                    )
                if self._gdst.gdst_RightShutOff == 1:
                    # Untensioning right
                    self.AdjustWithMinMax(
                        self._gdst.gdst_rightTensionInput,
                        self.susDownSpeed,
                        self.min_distance_mm,
                        self.max_distance_mm,
                    )

            #### Suspension Height ####
            if self._gdst.gdst_LeftFrontDown == 0 and self._gdst.gdst_LeftFrontUp == 1:
                self.AdjustWithMinMax(
                    self._gdst.gdst_leftFrontInput,
                    self.susUpSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )
            elif (
                self._gdst.gdst_LeftFrontDown == 1 and self._gdst.gdst_LeftFrontUp == 0
            ):
                self.AdjustWithMinMax(
                    self._gdst.gdst_leftFrontInput,
                    self.susDownSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )

            if self._gdst.gdst_LeftRearDown == 0 and self._gdst.gdst_LeftRearUp == 1:
                self.AdjustWithMinMax(
                    self._gdst.gdst_leftRearInput,
                    self.susUpSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )
            elif self._gdst.gdst_LeftRearDown == 1 and self._gdst.gdst_LeftRearUp == 0:
                self.AdjustWithMinMax(
                    self._gdst.gdst_leftRearInput,
                    self.susDownSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )

            if (
                self._gdst.gdst_RightFrontDown == 0
                and self._gdst.gdst_RightFrontUp == 1
            ):
                self.AdjustWithMinMax(
                    self._gdst.gdst_rightFrontInput,
                    self.susUpSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )
            elif (
                self._gdst.gdst_RightFrontDown == 1
                and self._gdst.gdst_RightFrontUp == 0
            ):
                self.AdjustWithMinMax(
                    self._gdst.gdst_rightFrontInput,
                    self.susDownSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )

            if self._gdst.gdst_RightRearDown == 0 and self._gdst.gdst_RightRearUp == 1:
                self.AdjustWithMinMax(
                    self._gdst.gdst_rightRearInput,
                    self.susUpSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )
            elif (
                self._gdst.gdst_RightRearDown == 1 and self._gdst.gdst_RightRearUp == 0
            ):
                self.AdjustWithMinMax(
                    self._gdst.gdst_rightRearInput,
                    self.susDownSpeed,
                    self.min_distance_mm,
                    self.max_distance_mm,
                )

            self.LeftTensionPressure = self.ConvertBarToMilliVoltage(
                self._gdst.gdst_leftTensionInput
            )
            self.RightTensionPressure = self.ConvertBarToMilliVoltage(
                self._gdst.gdst_rightTensionInput
            )

            self.LeftFrontDisp = self.ConvertMmToMilliVoltage(
                self._gdst.gdst_leftFrontInput
            )
            self.LeftRearDisp = self.ConvertMmToMilliVoltage(
                self._gdst.gdst_leftRearInput
            )
            self.RightFrontDisp = self.ConvertMmToMilliVoltage(
                self._gdst.gdst_rightFrontInput
            )
            self.RightRearDisp = self.ConvertMmToMilliVoltage(
                self._gdst.gdst_rightRearInput
            )

            ################# JUST FOR TESTING AND COMPARE ##################
            self._gdst.LeftTensionPressure_pot = self.volt_to_pot(
                self.LeftTensionPressure
            )
            self._gdst.RightTensionPressure_pot = self.volt_to_pot(
                self.RightTensionPressure
            )
            self._gdst.LeftFrontDisp_pot = self.volt_to_pot(self.LeftFrontDisp)
            self._gdst.LeftRearDisp_pot = self.volt_to_pot(self.LeftRearDisp)
            self._gdst.RightFrontDisp_pot = self.volt_to_pot(self.RightFrontDisp)
            self._gdst.RightRearDisp_pot = self.volt_to_pot(self.RightRearDisp)
            #################################################################

            # ~ if self._gdst.testing_active == 0:
            # ~ self._io.data_to_board(800, self.volt_to_pot(self.RightRearDisp))
            # ~ self._io.data_to_board(808, self.volt_to_pot(self.LeftRearDisp))
            # ~ self._io.data_to_board(809, self.volt_to_pot(self.RightFrontDisp))
            # ~ self._io.data_to_board(810, self.volt_to_pot(self.LeftFrontDisp))
            # ~ self._io.data_to_board(811, self.volt_to_pot(self.LeftTensionPressure))
            # ~ self._io.data_to_board(812, self.volt_to_pot(self.RightTensionPressure))
