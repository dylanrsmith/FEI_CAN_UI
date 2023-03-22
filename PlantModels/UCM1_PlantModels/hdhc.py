class hdhc_plant:
    def __init__(self, ob1, ob2):
        self._hc = ob1
        self._io = ob2
        self.lateral_position_cur = 0
        self.hdr_cw_valve_threshold_cur = 550
        self.hdhr_hdr_ccw_threshold_cur = 550
        self.current_frd_angle_volt = 0
        self.current_lateral_tilt_voltage = 0
        self.current_headerwidth = 0
        self.MaxExtension_mm = 40
        self.current_MaxExtension_mm = 40
        self.Mm2PixelsScaling = 700.0 / 15000.0
        self.max_cur_cw = 5
        self.max_cur_ccw = 5
        self.hdhc_adc_to_cur_cw = 0
        self.hdhc_adc_to_cur_ccw = 0

        ## header plates function - comments these later if not find in use
        self.lateral_tilt_angle = 0
        self.norm_halfheaderwidth = 0
        self.norm_MaxExtension_mm = 0
        self.offset = 0
        self.HeaderLeft = 0
        self.HeaderRight = 0

    def volt_to_pot(self, volt):
        pot_value = round((volt / 1000) * 250 / 4.864)
        return pot_value

    def header_plates(self, hdr_width, feeder_angle_voltage, lateral_tilt_voltage):
        if (
            (self.current_frd_angle_volt != feeder_angle_voltage)
            or (self.current_lateral_tilt_voltage != lateral_tilt_voltage)
            or (self.current_headerwidth != hdr_width)
            or (self.current_MaxExtension_mm != self._hc.hdhc_skid_plate_range)
        ):
            self.current_frd_angle_volt = feeder_angle_voltage
            self.current_frd_angle_volt = feeder_angle_voltage
            self.current_lateral_tilt_voltage = lateral_tilt_voltage
            self.current_MaxExtension_mm = self._hc.hdhc_skid_plate_range

            self.lateral_tilt_angle = -(
                (self.current_lateral_tilt_voltage - 2500.0)
                * 5.0
                / (2500.0 - 1100.0)
                * (3.14)
                / 180.0
            )
            self.norm_halfheaderwidth = self.headerwidth_mm * self.Mm2PixelsScaling / 2
            self.norm_MaxExtension_mm = (
                self.current_MaxExtension_mm * self.Mm2PixelsScaling
            )
            self.offset = (feeder_angle_voltage - 1500) * 120 / 4000
            self.HeaderLeft = self.norm_halfheaderwidth
            self.HeaderRight = self.norm_halfheaderwidth

    def calculate(self):
        ### Feeder Angle
        if self._hc.hdhc_frd_ang_enabled == 1:
            if self._hc.testing_active == 0:
                self._hc.hdhc_flow_cmd_extend = 0  # self._io.data_read(115) #dummy spn
                self._hc.hdhc_flow_cmd_retract = 0  # self._io.data_read(115) #dummy spn
                self._hc.hdhc_flow_pct = 0  # self._io.data_read()

            if self._hc.hdhc_flow_cmd_extend > 0:
                self._hc.hdhc_feeder_angle_volt += self._hc.hdhc_flow_pct
            if self._hc.hdhc_flow_cmd_retract > 0:
                #### is header ground 0 is checked!! here
                self._hc.hdhc_feeder_angle_volt -= self._hc.hdhc_flow_pct

            if self._hc.hdhc_feeder_angle_volt < 500:
                self._hc.hdhc_feeder_angle_volt = 500
            elif self._hc.hdhc_feeder_angle_volt > 4400:
                self._hc.hdhc_feeder_angle_volt = 4400

        ### Lateral Float
        if self._hc.hdhc_lat_float_enabled == 1:
            if self._hc.testing_active == 0:
                self._hc.hdhc_lateral_float_cw = self._io.data_read(117)
                self._hc.hdhc_lateral_float_ccw = self._io.data_read(118)

            self.hdhc_adc_to_cur_cw = (
                self._hc.hdhc_lateral_float_cw * self.max_cur_cw / 1024 * 1000
            )
            self.hdhc_adc_to_cur_ccw = (
                self._hc.hdhc_lateral_float_ccw * self.max_cur_ccw / 1024 * 1000
            )

            self.hdhc_deltaV = 0
            if self._hc.hdhc_lateral_float_cw > self.hdr_cw_valve_threshold_cur:
                self.hdhc_deltaV += (
                    (self.hdhc_adc_to_cur_cw - self.hdr_cw_valve_threshold_cur)
                    * 0.3385
                    * 0.01
                )  # The 0.01 multiplication is due to the plantmodel is running @10ms.
            if self._hc.hdhc_lateral_float_ccw > self.hdhr_hdr_ccw_threshold_cur:
                self.hdhc_deltaV -= (
                    (self.hdhc_adc_to_cur_cw - self.hdhr_hdr_ccw_threshold_cur)
                    * 0.3385
                    * 0.01
                )

            self.lateral_position_cur += self.hdhc_deltaV

            if self.lateral_position_cur > 4000:
                self.lateral_position_cur = 4000
            if self.lateral_position_cur < 1000:
                self.lateral_position_cur = 1000

            self._hc.hdhc_lateral_position_volt = self.lateral_position_cur

        # ### Header Model
        # self.header_plates()

        ### Lift Pressure
        if self._hc.hdhc_lift_pressure_enabled == 1:
            if self._hc.testing_active == 0:
                if self._hc.hdhc_feeder_angle_volt < 1900:
                    self._hc.hdhc_lift_prs_volt = 500  # 0bar
                elif self._hc.hdhc_feeder_angle_volt > 4300:
                    self._hc.hdhc_lift_prs_volt = 3700  # 200 bar
                elif (
                    self._hc.hdhc_feeder_angle_volt > 1900
                    and self._hc.hdhc_feeder_angle_volt < 4300
                ):
                    self._hc.hdhc_lift_prs_volt = 2100  # 100 bar

        #### Ground Height Sensor
        if self._hc.hdhc_gnd_height_enabled == 1:
            ## Read from eeprom settings
            # self._hc.l_header_type_e
            # self._hc.l_header_platform_type_e

            if self._hc.hdhc_header_platform_type == 0:  # Rigid
                if self._hc.hdhc_feeder_angle_volt == 1850:
                    self._hc.hdhc_rh_height_tilt_volt = 1000
                if self._hc.hdhc_feeder_angle_volt == 2500:
                    self._hc.hdhc_rh_height_tilt_volt = 4250
            elif self._hc.hdhc_header_platform_type == 1:  # Flex
                if self._hc.hdhc_feeder_angle_volt == 1850:
                    self._hc.hdhc_rh_height_tilt_volt = 4250
                if self._hc.hdhc_feeder_angle_volt == 2500:
                    self._hc.hdhc_rh_height_tilt_volt = 1000

            if self._hc.hdhc_feeder_angle_volt == 1850:
                self._hc.hdhc_lh_height_tilt_volt = 1000
            elif self._hc.hdhc_feeder_angle_volt == 2500:
                self._hc.hdhc_lh_height_tilt_volt = 4250

            if self._hc.hdhr_type == 1:
                self._hc.hdhc_center_rh_height_volt = 0
            elif self._hc.hdhr_type != 0:
                if self._hc.hdhc_feeder_angle_volt == 1850:
                    self._hc.hdhc_center_rh_height_volt = 1000
                elif self._hc.hdhc_feeder_angle_volt == 2500:
                    self._hc.hdhc_center_rh_height_volt = 4250

            if self._hc.hdhc_feeder_angle_volt == 1850:
                self._hc.hdhc_center_lh_height_volt = 1000
            elif self._hc.hdhc_feeder_angle_volt == 2500:
                self._hc.hdhc_center_lh_height_volt = 4250

        ################# JUST FOR TESTING AND COMPARE ##################
        self._hc.hdhc_lift_prs_volt_pot = self.volt_to_pot(self._hc.hdhc_lift_prs_volt)
        self._hc.hdhc_feeder_angle_volt_pot = self.volt_to_pot(
            self._hc.hdhc_feeder_angle_volt
        )
        self._hc.hdhc_lh_height_tilt_volt_pot = self.volt_to_pot(
            self._hc.hdhc_lh_height_tilt_volt
        )
        self._hc.hdhc_center_lh_height_volt_pot = self.volt_to_pot(
            self._hc.hdhc_center_lh_height_volt
        )
        self._hc.hdhc_center_rh_height_volt_pot = self.volt_to_pot(
            self._hc.hdhc_center_rh_height_volt
        )
        self._hc.hdhc_rh_height_tilt_volt_pot = self.volt_to_pot(
            self._hc.hdhc_rh_height_tilt_volt
        )
        self._hc.hdhc_lateral_position_volt_pot = self.volt_to_pot(
            self._hc.hdhc_lateral_position_volt
        )
        ####################################################################

        # ~ if self._hc.testing_active == 0:
        # ~ self._io.data_to_board(57, self.volt_to_pot(self._hc.hdhc_lift_prs_volt))
        # ~ self._io.data_to_board(60, self.volt_to_pot(self._hc.hdhc_feeder_angle_volt))
        # ~ self._io.data_to_board(71, self.volt_to_pot(self._hc.hdhc_lh_height_tilt_volt))
        # ~ self._io.data_to_board(72, self.volt_to_pot(self._hc.hdhc_center_lh_height_volt))
        # ~ self._io.data_to_board(77, self.volt_to_pot(self._hc.hdhc_center_rh_height_volt))
        # ~ self._io.data_to_board(78, self.volt_to_pot(self._hc.hdhc_rh_height_tilt_volt))
        # ~ self._io.data_to_board(58, self.volt_to_pot(self._hc.hdhc_lateral_position_volt))
