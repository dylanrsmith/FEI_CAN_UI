import time  # Ifdef # remove "import time" in final version
from datetime import datetime

dip_flag = 0
IncrVoltage = 0
rise_flag = 0
diffrence_voltage = 0


class rotor_hydro:
    global _rotor, _io
    prevRotorRPM = 0
    RotorRPM = 0
    TrueRotorRPM = 0
    RotorCombinedRPM = 0
    FeedRollRPM = 0
    log_enable = 0
    log_file_index = 0
    if log_enable == 1:
        log_file = open(
            "/home/pi/Desktop/Bench_Code/PlantModels/UCM2_PlantModels/rotor_current_log.csv",
            "a",
        )

    #     Flag_Start = 0 # Ifdef
    #     Flag_End = 0
    #     Rotor_Start_Time = 0
    #     Rotor_Stop_Time = 0
    #     CounterDifferenceStartTime = 0

    def __init__(self, ob1, ob2):
        self._rotor = ob1
        self._io = ob2

    def RotorPWMToFDispl(self, PWM):
        """

        :param PWM:
        :return:
        """
        flow = 0
        # print('PWM : ' , PWM)
        if PWM > 0.93:
            if PWM < 2.76:
                flow = (90 / (2.76 - 0.93)) * (PWM - 0.93)
            else:
                flow = (90 / (2.76 - 0.93)) * (2.76 - 0.93)  # see comment on line448
        else:  # No need of else if declred above "flow = 0"
            flow = 0
        return flow

    def RotorDisplToRPM(self, displ, incr, decr, ERPM):
        """

        :param displ:
        :param incr:
        :param decr:
        :param ERPM:
        :return:
        """
        RPM = 200
        flow = displ * ERPM * 1.355
        if flow != 0:
            if incr == 1:
                TrueRPM = int(flow / 63)
                if TrueRPM <= 2380:
                    RPM = int(TrueRPM * 72 / 2060)
                if TrueRPM > 2380:
                    RPM = int(TrueRPM * 12 / 980) + 54
            else:
                if decr == 1:
                    TrueRPM = -int(flow / 63)
                    if TrueRPM <= 2380:
                        RPM = -int(TrueRPM * 72 / 2060)
                    if TrueRPM > 2380:
                        RPM = -int(TrueRPM * 12 / 980) + 54
                else:
                    RPM = 200
        else:
            RPM = 200
            TrueRPM = 0
        if RPM > self._rotor.max_rotor_spd:
            RPM = self._rotor.max_rotor_spd
        return RPM, TrueRPM

    def RPMAdaptation(self, Value):
        """

        :param Value:
        :return:
        """
        newRPM = Value * 300 * 94
        return newRPM

    def RotorClutchRPM(self, PWM, ERPM, clutchon):
        """

        :param PWM:
        :param ERPM:
        :param clutchon:
        :return:
        """
        if clutchon == 1:
            if PWM > 0.83:
                RPM = int(ERPM * 1.1356 * 0.833)
            else:
                RPM = 0
        else:
            RPM = 0
        return RPM

    def getIncrCurrentFromvoltage(self, inputvoltage, offset, scalefactor, RotorIncr):
        global dip_flag
        global IncrVoltage
        global rise_flag
        global diffrence_voltage

        if RotorIncr == 0:
            return 0
        elif RotorIncr == 1 and inputvoltage < 1.2060546875:
            if dip_flag == 0:
                IncrVoltage = 1.220703125  # (247*(5/1024)) + (3*(5/1024))
                dip_flag = 1
            elif dip_flag == 1:
                IncrVoltage = IncrVoltage + 0.0146484375  # (3*(5/1024))
            return abs(((IncrVoltage - 1.2060546875) * scalefactor))
        elif RotorIncr == 1 and inputvoltage >= 1.2060546875:
            if rise_flag == 0:
                diffrence_voltage = IncrVoltage - inputvoltage
                IncrVoltage = inputvoltage + diffrence_voltage
                rise_flag = 1
            elif rise_flag == 1:
                IncrVoltage = inputvoltage + diffrence_voltage
                if IncrVoltage > 1.923828125:
                    IncrVoltage = 1.923828125
            return abs(((IncrVoltage - 1.2060546875) * scalefactor))
        else:
            return 0

    #         # compared with pc sim: voltage goes from 1.2V to 1.9V, current should be from 0 to 1.1A
    #         inputvoltage = inputvoltage-offset
    #         if (inputvoltage < 0 or RotorIncr == 0):
    #             return 0
    #         elif(abs(inputvoltage) > 0 and RotorIncr == 1):
    #             return (abs(inputvoltage) * scalefactor)
    #         else:
    #             return 0

    def getDecrCurrentFromvoltage(self, inputvoltage, offset, scalefactor, RotorDecr):
        # compared with pc sim: voltage goes from 1.2V to 1.9V, current should be from 0 to 1.1A
        inputvoltage = inputvoltage - offset
        if inputvoltage < 0 or RotorDecr == 0:
            return 0
        elif abs(inputvoltage) > 0 and RotorDecr == 1:
            return abs(inputvoltage) * scalefactor
        else:
            return 0

    # look up tables
    def getIncDisplacementVolume(self, current):
        if current < 0.400:
            return current / 0.4 * 0.042
        elif current < 1100:
            return (current - 1.1) / (1.1 - 0.4) * 134 + 0.042
        elif current < 1200:
            return (current - 1.1) / (1.2 - 1.1) * (154 - 134) + 134
        else:
            return (current - 1.2) / (5 - 1.2) * (300 - 154) + 154

    def getDecDisplacementVolume(self, current):
        rval = 0
        if current < 0.400:
            return current / 0.4 * 0.042
        elif current < 1100:
            return (current - 1.1) / (1.1 - 0.4) * 120 + 0.042
        elif current < 1200:
            return (current - 1.1) / (1.2 - 1.1) * (135 - 120) + 120
        else:
            return (current - 1.2) / (5 - 1.2) * (300 - 135) + 135

    HydroMotorSpeed = 0
    prevHydroMotorSpeed = -1

    RotorSpeed = 0
    prevRotorSpeed = -1

    RingTeeth = 63
    SunTeeth = 13
    PlanetTeeth = 24

    value1 = 0
    value2 = 0

    statediagram_value = 0
    prevAuxProSts = 0
    prevRTFSts = 0

    def calculate_rotor(self):
        global dip_flag
        global IncrVoltage
        global rise_flag
        global diffrence_voltage

        RotorIncr = self._io.data_read(418)

        RotorDecr = self._io.data_read(419)

        AuxPTOValveOn = self._io.data_read(417)

        input_duty = 0
        etr_clutch = 0
        rtf_clutch = 0

        motorvolume = 50

        if self.statediagram_value == 0:
            if self.prevAuxProSts == 0 and AuxPTOValveOn == 1:
                self.statediagram_value = 1
        elif self.statediagram_value == 1:
            if self.prevRTFSts == 0 and RotorIncr == 1:
                self.statediagram_value = 2
        elif self.statediagram_value == 2:
            if self.prevRTFSts == 1 and RotorIncr == 0:
                self.statediagram_value = 3
        elif self.statediagram_value == 3:
            if self.prevAuxProSts == 1 and AuxPTOValveOn == 0:
                self.statediagram_value = 0
                dip_flag = 0
                IncrVoltage = 0
                rise_flag = 0
                diffrence_voltage = 0

        self.prevAuxProSts = AuxPTOValveOn
        self.prevRTFSts = RotorIncr

        hydro_vlt_inc = self._io.data_read(375) * 5 / 1024
        hydro_vlt_dec = self._io.data_read(377) * 5 / 1024
        etr_clutch_current = self._io.data_read(376) * 5 / 1024
        rtf_clutch_current = self._io.data_read(393) * 5 / 1024

        etr_on = self._io.data_read(420) == 1
        rtf_on = rtf_clutch_current > 1.0

        # calculate hydro motor speed
        hydro_current_inc = self.getIncrCurrentFromvoltage(
            hydro_vlt_inc, 1.2, 1.2 / 0.736, RotorIncr
        )
        hydro_current_dec = self.getDecrCurrentFromvoltage(
            hydro_vlt_dec, 1.2, 1.0 / 1.2, RotorDecr
        )

        volumeRotationPump = self.getIncDisplacementVolume(
            hydro_current_inc
        ) - self.getDecDisplacementVolume(hydro_current_dec)
        volumeFloating = volumeRotationPump * self._rotor.current_spd  # 1000 #ERPM

        # if aux pto is ont and rtf is on, hydro motor speed is 1774
        if self.statediagram_value == 2:
            self.HydroMotorSpeed = 3200
        elif self.statediagram_value == 3:
            self.HydroMotorSpeed = volumeFloating / motorvolume
        else:
            self.HydroMotorSpeed = 0

        #        print("\nHydro Motor Speed : ", self.HydroMotorSpeed)

        ringspeed = 0
        if rtf_on:
            ringspeed = 0
        elif etr_on:
            ringspeed = self._rotor.current_spd  # 1000 # ERPM

        if rtf_on or etr_on:
            # 67.0 / 59.0 = MainGbx3 output
            self.RotorSpeed = (
                self.RingTeeth
                / (self.SunTeeth + self.RingTeeth)
                * ringspeed
                * 67.0
                / 59.0
                + self.SunTeeth
                / (self.SunTeeth + self.RingTeeth)
                * self.HydroMotorSpeed
            )
        else:
            # slowing down exponential
            self.RotorSpeed = 99.95 * self.RotorSpeed / 100.0

        # gearbox
        self.RotorSpeed = self.RotorSpeed * 19.0 / 73.0  # Gear 1
        # self.RotorSpeed = self.RotorSpeed * 21.0 / 55.0  # Gear 2
        # self.RotorSpeed = self.RotorSpeed * 27.0 / 50.0  # Gear 3

        if self.RotorSpeed < 0:
            self.RotorSpeed = -self.RotorSpeed

        if self.RotorSpeed != int(self.prevRotorSpeed):
            self.prevRotorSpeed = self.RotorSpeed

            if int(self.RotorSpeed) < 1:
                # send 200 to disable the PWM
                # rotor speed
                self._io.data_to_board(347, 200)
                # feedrol
                self._io.data_to_board(349, 200)
            else:
                # linear curve value (rpm) to pwm (of the potmeter): 0.0694x-0.5187
                self.value2 = 0.0694 * self.RotorSpeed - 0.5187

                if self.value2 < 0:
                    self.value2 = 200

                self._io.data_to_board(347, round(self.value2))
                # feedrol
                self._io.data_to_board(349, round(self.value2))

        if self.HydroMotorSpeed < 0:
            self.HydroMotorSpeed = -self.HydroMotorSpeed

        if self.HydroMotorSpeed != self.prevHydroMotorSpeed:
            self.prevHydroMotorSpeed = self.HydroMotorSpeed

            if int(self.HydroMotorSpeed) < 1:
                # send 200 to disable the PWM
                self._io.data_to_board(348, 200)
            else:
                # linear curve from spi data to PWM: 0.0213x-0.4556
                self.value1 = 0.0213 * self.HydroMotorSpeed - 0.4556
                if self.value1 < 0:
                    self.value1 = 200
                self._io.data_to_board(348, round(self.value1))
                # self._io.data_to_board(348, int(self.value1 + 0.5))

        # Log to excel
        if self.log_enable == 1:
            self.log_file.write(
                "{0},{1},{2},{3}\n".format(
                    str(self.log_file_index),
                    str(hydro_current_inc),
                    str(hydro_current_dec),
                    str(self.HydroMotorSpeed),
                )
            )
            self.log_file_index = self.log_file_index + 1

        # print(hydro_vlt_inc, hydro_current_inc, RotorIncr, hydro_vlt_dec, hydro_current_dec, RotorDecr, rtf_on, etr_on, AuxPTOValveOn, self._rotor.current_spd, self.HydroMotorSpeed, self.RotorSpeed)

    #         RotorClutchOn = self._io.data_read(420)
    #         if RotorIncr == 1:
    #             temp = self._io.data_read(375) * 5/1024
    #             if temp > 0.93:
    #                 input_duty = temp
    #             else: # No need of else
    #                 input_duty = 0
    #         if RotorDecr == 1:
    #             temp = self._io.data_read(377) * 5/1024
    #             if temp > 0.93:
    #                 input_duty = temp
    #             else: # No need of else
    #                 input_duty = 0
    #         if RotorClutchOn == 1:
    #             temp = self._io.data_read(376) * 5/1024
    #             if temp > 0.93:
    #                 etr_clutch = temp
    #             else: # No need of else
    #                 etr_clutch = 0
    #         if self._rotor.reverserEngaged == 0:
    # #             print('self._rotor.reverserEngaged : ' , self._rotor.reverserEngaged)
    #             if (RotorIncr == 1 or RotorDecr == 1) and AuxPTOValveOn == 1:
    # #                if self.Flag_Start == 0:
    # #                    self.Rotor_Start_Time = time.time()
    # #                    self.Flag_Start = 1
    #                #print('self.counter : ' , self.counter)
    #                 self.counter += 1
    #                 if self.counter > 12:
    # #                    print("In normal control")
    #                     RotorDispl = self.RotorPWMToFDispl(input_duty)   # Calculate before thesetting any values i.e. when counter < 1
    # #                     print('RotorDispl : ' , RotorDispl)
    #                     self.RotorRPM, self.TrueRotorRPM = self.RotorDisplToRPM(RotorDispl, RotorIncr, RotorDecr, self._rotor.current_spd)
    # #                     print('RotorRPM : ' , self.RotorRPM)
    # #                     print('True RotorRPM : ' , self.TrueRotorRPM)
    #                     if self.RotorRPM > self.prevRotorRPM:
    #                         self._io.data_to_board(348, abs(self.RotorRPM))
    #                         self.prevRotorRPM = self.RotorRPM
    # #                        if self.Flag_End == 0:
    # #                            self.Rotor_Stop_Time = time.time()
    # #                            print("Cycle Time : \t",(self.Rotor_Stop_Time - self.Rotor_Start_Time))
    # #                            self.Flag_End = 1
    #                     else:
    #                         if abs(self.RotorRPM - self.prevRotorRPM) > 4:
    #                             self._io.data_to_board(348, abs(self.RotorRPM))
    #                             self.prevRotorRPM = self.RotorRPM
    # #                        if self.Flag_End == 0:
    # #                            self.Rotor_Stop_Time = time.time()
    # #                            print("Cycle Time : \t",(self.Rotor_Stop_Time - self.Rotor_Start_Time))
    # #                            self.Flag_End = 1
    #                 else:
    #
    #                     if self.counter == 1:
    #                         print("SPN  = 347")
    #                         self._io.data_to_board(347, 11) # 196rpm # Replace with write potmeter function
    # #                        self.CounterDifferenceStartTime = time.time()
    # #                        time.sleep(0.015)
    #                     if self.counter == 2:
    #                         print("SPN  = 348")
    #                         self._io.data_to_board(348, 36) # Replace with write potmeter function
    # #                        print("Counter Diffrence : \t",time.time()- self.CounterDifferenceStartTime)
    #                     self.TrueRotorRPM = 1696 # 1692 #1670 #1924
    #
    #                     if self.counter > 13: # Remove
    # #                        print("In reset counter************************************************")
    #                         self.counter = 0
    #             else:
    #                 self.writepotmeterRPM_fn(348, 200, self.RotorRPM)
    #                 self.RotorRPM = 200
    #                 self.counter = 0
    #                 self.Flag_Start = 0 # Ifdef
    #                 self.Flag_End = 0
    #                 self.Rotor_Start_Time = 0
    #                 self.Rotor_Stop_Time = 0
    #         else:
    #             if (RotorIncr == 1 or RotorDecr == 1) and AuxPTOValveOn == 1:
    #                 RotorDispl = self.RotorPWMToFDispl(input_duty)
    # #                 print('RotorDispl : ' , RotorDispl)
    #                 self.RotorRPM, self.TrueRotorRPM = self.RotorDisplToRPM(RotorDispl, RotorIncr, RotorDecr, self._rotor.current_spd)
    # #                 print('RotorRPM : ' , self.RotorRPM)
    # #                 print('True RotorRPM : ' , self.TrueRotorRPM)
    #                 if self.RotorRPM > self.prevRotorRPM:
    #                     self._io.data_to_board(348, abs(self.RotorRPM))
    #                     self.prevRotorRPM = self.RotorRPM
    #                 else:
    #                     if abs(self.RotorRPM - self.prevRotorRPM) > 4:
    #                         self._io.data_to_board(348, abs(self.RotorRPM))
    #                         self.prevRotorRPM = self.RotorRPM
    #             else:
    #                 self.writepotmeterRPM_fn(348, 200, self.RotorRPM)
    #                 self.RotorRPM = 200
    #         if RotorClutchOn == 1:
    #             RotorETRRPM = self.RotorClutchRPM(etr_clutch, self._rotor.current_spd, RotorClutchOn)
    #         else:
    #             RotorETRRPM = 200
    #         if self.RotorRPM == 200 and RotorETRRPM == 200:
    #             self.writepotmeterRPM_fn(347, 200, self.RotorCombinedRPM)
    #             self.RotorCombinedRPM = 200
    #         if self.RotorRPM != 200 and RotorETRRPM == 200:
    #             self.writepotmeterRPM_fn(347, abs(int((self.TrueRotorRPM * 20 / 300 * 0.099)*self._rotor.rotor_gear_box)), abs(self.RotorCombinedRPM))
    #             self.RotorCombinedRPM = int(self.TrueRotorRPM * 20 / 300 * 0.099)
    #             #print("self._rotor.rotor_gear_box : ", self._rotor.rotor_gear_box)
    # #             print('RotorCombinedRPM 1: ', self.RotorCombinedRPM)#was17
    # #             print('TrueRotorRPM 1: ', self.TrueRotorRPM)#was17
    #         if self.RotorRPM == 200 and RotorETRRPM != 200:
    #             if self._rotor.ThreshingRotorStatus == 3:
    #                 self.writepotmeterRPM_fn(347, 200, self.RotorCombinedRPM)
    #                 self.RotorCombinedRPM = 200
    #             else:
    #                 self.writepotmeterRPM_fn(347, int(RotorETRRPM / 14.3 * 0.596),
    #                                  self.RotorCombinedRPM)
    #                 self.RotorCombinedRPM = int(RotorETRRPM / 14.3 * 0.596)
    #         if self.RotorRPM != 200 and RotorETRRPM != 200:
    #             #print("etrpm", self._rotor.rotor_gear_box)
    #             self.writepotmeterRPM_fn(347, int(((RotorETRRPM / 14.3 * 0.596) + (self.TrueRotorRPM * 20 / 300 * 0.099)) * self._rotor.rotor_gear_box),
    #                              self.RotorCombinedRPM)
    #             self.RotorCombinedRPM = int(((RotorETRRPM / 14.3 * 0.596) + (self.TrueRotorRPM * 20 / 300 * 0.099)))
    #
    #         if self.RotorCombinedRPM <= 75:
    #             self.writepotmeterRPM_fn(349, abs(int(((self.RotorCombinedRPM / 1.37) * 1.045) * (self._rotor.rotor_gear_box) * (1-(self._rotor.feed_roll/100)))), self.FeedRollRPM)
    #             self.FeedRollRPM = int(
    #                 (self.RotorCombinedRPM / 1.37) * 1.045)
    #
    # #         if self.RotorCombinedRPM == 0:
    # #             self._io.data_to_board(349, 200)
    #
    #         else:
    #             if self.RotorCombinedRPM > 75:
    #                 self.writepotmeterRPM_fn(349, abs(int(((self.RotorCombinedRPM / 1.28) * 1.045) * (self._rotor.rotor_gear_box) * (1-(self._rotor.feed_roll/100)))), self.FeedRollRPM)
    #                 self.FeedRollRPM = int(
    #                     (self.RotorCombinedRPM / 1.28) * 1.045)
    #
    #             else:
    #                 self._io.data_to_board(349, 200)

    def writepotmeterRPM_fn(self, td, value, prevValue):
        """

        :param td:
        :param value:
        :param prevValue:
        """
        if prevValue != value:
            self._io.data_to_board(td, value)

        # IFdef 121


#        if AuxPTOValveOn == 1 and self.Flag_End_AuxPTOValveOn == 0:
#            self.EndAuxPTOValveOn = time.time()
#            print("AuxPTOValveOn Time : \t",self.EndAuxPTOValveOn-self.StartAuxPTOValveOn)
#            self.Flag_End_AuxPTOValveOn = 1
# End IFdef 131

# IFdef 104
#        if RotorIncr == 0 and self.Flag_Start_RotorIncr == 0:
#            self.StartRotorIncr = time.time()
#            print("StartRotorIncr : \t",self.StartRotorIncr)
#            self.Flag_Start_RotorIncr = 1

#        if RotorIncr == 1 and self.Flag_End_RotorIncr == 0:
#            self.EndRotorIncr = time.time()
#            self.Flag_End_RotorIncr = 1
#            print("RotorIncr Time : \t",self.EndRotorIncr - self.StartRotorIncr)
# End IFdef            114
