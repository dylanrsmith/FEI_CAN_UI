class Feeder_hydro:
    global _Feeder, _io
    EngineCVTInputRatio = (67 / 51) * (59 / 77)
    Engine_to_AuxPTO_Ratio = 67 / 55
    AuxPTO_to_FeederPump_GearRatio = (34 / 33) * (27 / 25)
    Header_JackShaft_Gbx = 14 / 39
    Ring_Teeth = 65
    Sun_Teeth = 13
    Planet_Teeth = 25
    Feeder_Pump_Max_Displacement = 45
    Feeder_Motor_Displacement = 37  # Motor Volume
    MAX_Engine_RPM = 1900
    Feeder_Speed_Setpoint = 690
    Cal_Feeder_Motor_RPM = 0
    Cal_Feeder_RPM = 0

    """ Process Variables"""
    AuxPTOValveOn = 0
    FeederClutchOn = 0
    FeederIncr = 0
    FeederDecr = 0

    Prev_AuxPTOValveOn = 0
    Prev_FeederClutchOn = 0
    Prev_FeederIncr = 0
    Prev_FeederDecr = 0

    State_Diagram_Value = 0

    Engine_RPM = 0

    Feeder_RPM = 0
    Feeder_Motor_RPM = 0

    Hydro_INCR_Vlt = 0
    Hydro_DECR_Vlt = 0

    Hydro_INCR_Vlt_Offset = 1.23046875
    Hydro_INCR_Vlt_ScaleFactor = (1.191 - 0.473) / (3.18359375 - 1.23046875)

    Hydro_DECR_Vlt_Offset = 1.23046875
    Hydro_DECR_Vlt_ScaleFactor = (1.191 - 0.473) / (3.18359375 - 1.23046875)

    VolumeRotationPump = 0
    VolumeFloating = 0
    """  Debug Variables
    Check the need after testing"""
    counter = 0
    TopShaft_Type = "Normal"  # "Normal" OR "Slow"
    Feed_Roll = "Installed"  # "Installed" OR "Not Installed"
    TopShaft_to_JackShaft_Ratio = 0
    log_enable = 0
    log_file_index = 0
    if log_enable == 1:
        log_file = open(
            "/home/pi/Desktop/Bench_Code/PlantModels/UCM1_PlantModels/feeder.csv", "a"
        )

    if TopShaft_Type == "Normal" and Feed_Roll == "Installed":
        TopShaft_to_JackShaft_Ratio = 1.506

    elif TopShaft_Type == "Normal" and Feed_Roll == "Not Installed":
        TopShaft_to_JackShaft_Ratio = 1.873

    elif TopShaft_Type == "Slow" and Feed_Roll == "Installed":
        TopShaft_to_JackShaft_Ratio = 1.674

    elif TopShaft_Type == "Slow" and Feed_Roll == "Not Installed":
        TopShaft_to_JackShaft_Ratio = 0

    def __init__(self, ob1, ob2):
        self._Feeder = ob1
        self._io = ob2

    def Get_Hydro_INCR_Cur(
        self,
        Hydro_INCR_Vlt,
        Hydro_INCR_Vlt_Offset,
        Hydro_INCR_Vlt_ScaleFactor,
        FeederIncr,
    ):
        if FeederIncr == 1:
            if Hydro_INCR_Vlt <= Hydro_INCR_Vlt_Offset:
                Hydro_INCR_Vlt = Hydro_INCR_Vlt_Offset + (1 * 5 / 1024)
            return (Hydro_INCR_Vlt - Hydro_INCR_Vlt_Offset) * Hydro_INCR_Vlt_ScaleFactor
        else:
            return 0

    def Get_Hydro_DECR_Cur(
        self,
        Hydro_DECR_Vlt,
        Hydro_DECR_Vlt_Offset,
        Hydro_DECR_Vlt_ScaleFactor,
        FeederDecr,
    ):
        if FeederDecr == 1:
            if Hydro_DECR_Vlt <= Hydro_DECR_Vlt_Offset:
                Hydro_DECR_Vlt = Hydro_DECR_Vlt_Offset + (1 * 5 / 1024)
            return (Hydro_DECR_Vlt - Hydro_DECR_Vlt_Offset) * Hydro_DECR_Vlt_ScaleFactor
        else:
            return 0

    def Get_Hydro_INCR_Displacement(self, Hydro_INCR_Cur):
        if Hydro_INCR_Cur < 0.400:
            return Hydro_INCR_Cur / 0.4 * 0.014
        elif Hydro_INCR_Cur < 1:
            return (Hydro_INCR_Cur - 1) / (1 - 0.4) * 134 + 0.014
        elif Hydro_INCR_Cur < 1.2:
            return (Hydro_INCR_Cur - 1) / (1.2 - 1.1) * (154 - 134) + 134
        else:
            return (Hydro_INCR_Cur - 1.2) / (5 - 1.2) * (300 - 154) + 154

    def Get_Hydro_DECR_Displacement(self, Hydro_DECR_Cur):
        if Hydro_DECR_Cur < 0.400:
            return Hydro_DECR_Cur / 0.4 * 0.042
        elif Hydro_DECR_Cur < 1100:
            return (Hydro_DECR_Cur - 1.1) / (1.1 - 0.4) * 134 + 0.042
        elif Hydro_DECR_Cur < 1200:
            return (Hydro_DECR_Cur - 1.1) / (1.2 - 1.1) * (154 - 134) + 134
        else:
            return (Hydro_DECR_Cur - 1.2) / (5 - 1.2) * (300 - 154) + 154

    def calculate_Feeder(self):
        self.AuxPTOValveOn = self._io.data_read(417)  # Digital SPN
        self.FeederIncr = self._io.data_read(162)  # Digital SPN
        self.FeederDecr = self._io.data_read(163)  # Digital SPN
        self.FeederClutchOn = self._io.data_read(164)  # Digital SPN

        self.Hydro_INCR_Vlt = self._io.data_read(119) * 5 / 1024
        self.Hydro_DECR_Vlt = self._io.data_read(121) * 5 / 1024

        # print(self._io.data_read(121))

        self.Hydro_INCR_Cur = self.Get_Hydro_INCR_Cur(
            self.Hydro_INCR_Vlt,
            self.Hydro_INCR_Vlt_Offset,
            self.Hydro_INCR_Vlt_ScaleFactor,
            self.FeederIncr,
        )
        self.Hydro_DECR_Cur = self.Get_Hydro_DECR_Cur(
            self.Hydro_DECR_Vlt,
            self.Hydro_DECR_Vlt_Offset,
            self.Hydro_DECR_Vlt_ScaleFactor,
            self.FeederDecr,
        )

        self.VolumeRotationPump = self.Get_Hydro_INCR_Displacement(
            self.Hydro_INCR_Cur
        ) - self.Get_Hydro_DECR_Displacement(self.Hydro_DECR_Cur)
        self.VolumeFloating = (
            self.VolumeRotationPump * self._Feeder.current_spd
        )  # 1000 #ERPM

        if self.State_Diagram_Value == 0:
            if self.Prev_AuxPTOValveOn == 0 and self.AuxPTOValveOn == 1:
                self.State_Diagram_Value = 1
        if self.State_Diagram_Value == 1:
            if self.Prev_FeederClutchOn == 0 and self.FeederClutchOn == 1:
                self.State_Diagram_Value = 2  # Write Cal_Feeder_Speed
        if self.State_Diagram_Value == 2:
            if (self.Prev_FeederIncr == 0 and self.FeederIncr == 1) or (
                self.Prev_FeederDecr == 0 and self.FeederDecr == 1
            ):
                self.State_Diagram_Value = 3  # Write Cal_Feeder_Motor_Speed, then write feeder speed & motor speed based Incr & Decr
        if self.State_Diagram_Value == 3:
            if (
                self.Prev_FeederClutchOn == 1
                and self.FeederClutchOn == 0
                and self.AuxPTOValveOn == 1
            ):
                self.State_Diagram_Value = 1
        if self.Prev_AuxPTOValveOn == 1 and self.AuxPTOValveOn == 0:
            self.State_Diagram_Value = 0

        self.Prev_AuxPTOValveOn = self.AuxPTOValveOn
        self.Prev_FeederClutchOn = self.FeederClutchOn
        self.Prev_FeederIncr = self.FeederIncr
        self.Prev_FeederDecr = self.FeederDecr

        self.Engine_RPM = self._Feeder.current_spd

        if self.State_Diagram_Value == 0:  # No Feeder Engage
            self.Feeder_RPM = 0
            self.Feeder_Motor_RPM = 0
            self._io.data_to_board(92, 200)
            self._io.data_to_board(94, 200)

        if (
            self.State_Diagram_Value == 1
        ):  # No Feeder Engage Calculate Feeder RPM and Motor RPM using Feeder_Speed_Setpoint
            self.Feeder_RPM = 0
            self.Feeder_Motor_RPM = 0
            self._io.data_to_board(92, 200)
            self._io.data_to_board(94, 200)

            self.Cal_Feeder_Motor_RPM = (
                (self.Feeder_Speed_Setpoint / self.Header_JackShaft_Gbx)
                * (self.Ring_Teeth + self.Sun_Teeth)
                - self.MAX_Engine_RPM * self.EngineCVTInputRatio * self.Ring_Teeth
            ) / self.Sun_Teeth

            self.Cal_Feeder_RPM = (
                (
                    self.Cal_Feeder_Motor_RPM * self.Sun_Teeth
                    + (self.Engine_RPM * self.EngineCVTInputRatio * self.Ring_Teeth)
                )
                / (self.Ring_Teeth + self.Sun_Teeth)
            ) * (self.Header_JackShaft_Gbx)

        if self.State_Diagram_Value == 2:  # Feeder Engage and Write Cal_Feeder_RPM
            self.Feeder_RPM = self.Cal_Feeder_RPM
            self.Feeder_Motor_RPM = 0
            self._io.data_to_board(92, 84)  # 84 62
            self._io.data_to_board(94, 200)

        if (
            self.State_Diagram_Value == 3
        ):  # Feeder Engage and Write Cal_Feeder_Motor_RPM
            self.Feeder_RPM = self.Cal_Feeder_RPM
            self.Feeder_Motor_RPM = self.Cal_Feeder_Motor_RPM
            self._io.data_to_board(94, 60)  # 60 1

        if self.log_enable == 1:
            #            self.log_file.write("{0},{1},{2},{3}\n".format(str(self.log_file_index),str(self.State_Diagram_Value),str(self.Feeder_RPM),str( self.Feeder_Motor_RPM)))
            self.log_file.write(
                "{0},{1}\n".format(str(self.log_file_index), str(FeederIncrVlt))
            )
            self.log_file_index = self.log_file_index + 1
            # print(self.State_Diagram_Value, self.Feeder_RPM, self.Feeder_Motor_RPM)
