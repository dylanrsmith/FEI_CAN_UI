# from IOCtrl import *
from lut import *


class driveline:
    global _dv, _io

    _lut = lut()

    auger_list_spd = [50, 90, 140, 180, 220, 270, 310, 360, 460, 540, 600]
    auger_list_freq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

    elevator_list_spd = [50, 90, 140, 180, 220, 270, 310, 360, 450, 530]
    elevator_list_freq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95]

    rotor_spd_list_spd = [150, 290, 440, 580, 730, 870, 1020, 1150, 1500, 1820, 2190]
    rotor_spd_list_freq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

    rotor_motor_spd_list_spd = [
        300,
        590,
        880,
        1160,
        1450,
        1740,
        2020,
        2310,
        2920,
        3480,
        4200,
    ]
    rotor_motor_spd_list_freq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

    feeder_spd_list_spd = [50, 98, 146, 194, 242, 291, 339, 388, 495, 578, 713]
    feeder_spd_list_freq = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

    def __init__(self, ob1, ob2):
        self._dv = ob1
        self._io = ob2
        # print("init")

    def auger_cal(self, spd):
        if spd == 0:
            return 200
        elif spd > 600:
            return 100
        else:
            data = self._lut.get_val(self.auger_list_spd, self.auger_list_freq, spd)
            return data

    def elevator_cal(self, spd):
        if spd == 0:
            return 200
        elif spd > 530:
            return 95
        else:
            data = self._lut.get_val(
                self.elevator_list_spd, self.elevator_list_freq, spd
            )
            return data

    def feeder_cal(self, spd):
        if spd == 0:
            return 200
        elif spd > 713:
            return 100
        else:
            data = self._lut.get_val(
                self.feeder_spd_list_spd, self.feeder_spd_list_freq, spd
            )
            return data

    def write_speed(self):
        auger = self._dv.sp_val[24]
        elevator = self._dv.sp_val[14]
        feed = self._dv.sp_val[26]

        auger_spd = self.auger_cal(auger)
        elevator_spd = self.elevator_cal(elevator)
        feed_spd = self.feeder_cal(feed)

        self._io.data_to_board(64, auger_spd)
        self._io.data_to_board(65, elevator_spd)
        if self._dv.feeder_type == 0:  # fixed feeder drive
            self._io.data_to_board(92, feed_spd)

    def calculate_speeds(self, spd):
        """

        :param spd:
        """
        MainGbx_S7 = spd * 1.01
        MainGbx_S3 = spd * 1.14

        if self._dv.debug_mode == 0:
            self._dv.PTO_LSD = self._io.data_read(417)
            if self._dv.PTO_LSD == 0:
                self._dv.Aux_PTO_enabled = 0
            else:
                self._dv.PTO_HSD = self._io.data_read(383)
                if self._dv.PTO_HSD != 0:
                    self._dv.Aux_PTO_enabled = 1
                else:
                    self._dv.Aux_PTO_enabled = 0

        if self._dv.Aux_PTO_enabled == 1:  # aux pto on
            Aux_PTO = spd * 1.22
        else:
            Aux_PTO = 0

        Aux_PTO_Thresher = Aux_PTO * 1.03
        Pumps_ZE = Aux_PTO * 1.11

        Cross_Over_Belt = Aux_PTO_Thresher * 0.46
        Unload_Belt_Drive = Aux_PTO_Thresher * 0.43

        Integral_Chopper_Belt_Drive = 0
        Integral_Chopper = 0
        HHMC = 0
        if self._dv.chopper_type == 0:  # IC
            Integral_Chopper_Belt_Drive = Aux_PTO_Thresher * 1.26
            if self._dv.IC_gear == 0:
                Integral_Chopper = Integral_Chopper_Belt_Drive * 0.27
            else:
                Integral_Chopper = Integral_Chopper_Belt_Drive * 1.00
        else:
            HHMC_Belt_Drive = Aux_PTO_Thresher * 1.19
            if self._dv.HHMC_gear == 0:
                HHMC = HHMC_Belt_Drive * 0.35
            else:
                HHMC = HHMC_Belt_Drive * 1.41

        Unloading_stubshaft = Unload_Belt_Drive * 1.00
        if self._dv.unload_rate == 0:  # 4.5
            Unloading_Belt_Drive_2 = Unloading_stubshaft * 0.54
        else:
            Unloading_Belt_Drive_2 = Unloading_stubshaft * 0.78

        Unloading_Gbx = Unloading_Belt_Drive_2 * 0.59
        Unload_Tube = Unloading_Gbx * 1.00

        Unloading_Gbx_2 = Unloading_Belt_Drive_2 * 1.00
        Unl_Cross_Auger_Rear = Unloading_Gbx_2 * 0.40

        Beater_Belt_Drive = Cross_Over_Belt * 0.73

        Elevator_Drive_Belt = Cross_Over_Belt * 0.55
        Elevator_Cross_Shaft = Elevator_Drive_Belt * 1.00
        Grain_Elev_Top_Shaft = Elevator_Cross_Shaft * 0.44
        Bubble_Up = Elevator_Cross_Shaft * 0.55

        Cleaning_Belt_Drive = Cross_Over_Belt * 0.73
        Tailings_Cross_Auger_Rethresher = Cleaning_Belt_Drive * 1.00
        Tailing_Gearbox = Cleaning_Belt_Drive * 0.89
        Tailings_Incline_Auger = Tailing_Gearbox * 1.00
        Eccentric = Tailing_Gearbox * 0.38

        Main_Clean_Grain_Cross_Auger = Tailing_Gearbox * 0.64
        Auger_Belt_Drive = Main_Clean_Grain_Cross_Auger * 0.91
        XA_Clean_Grain_Cross_Auger = Auger_Belt_Drive * 1.00

        Feeder_Header_Gbx = 0
        Fdr_JackShaft = 0
        Feeder_Top_Shaft = 0
        Feeder_RPM = 0
        if self._dv.feeder_type == 0:  # fixed feeder drive
            Feeder_Header_Gbx = spd * 0.85
            Fdr_JackShaft = Feeder_Header_Gbx * 0.36
            Top_Shaft_Belt_Drive = Fdr_JackShaft * 0.53
            Feeder_Top_Shaft = Top_Shaft_Belt_Drive * 1.00
            Feeder_RPM = Feeder_Top_Shaft * 1.5

        if self._dv.clutch_on == 1:
            if self._dv.clutch_pwm > 0.83:
                RPM = int(spd * 1.1356 * 0.833)
            else:
                RPM = 0
        else:
            RPM = 0

        Clutch_RPM = RPM
        Rotor_RPM = 50
        self._dv.sp_val = [
            Aux_PTO,
            Aux_PTO_Thresher,
            Pumps_ZE,
            Cross_Over_Belt,
            Unload_Belt_Drive,
            Integral_Chopper,
            HHMC,
            Unloading_stubshaft,
            Unloading_Belt_Drive_2,
            Unloading_Gbx,
            Unl_Cross_Auger_Rear,
            Unloading_Gbx_2,
            Unl_Cross_Auger_Rear,
            Beater_Belt_Drive,
            Elevator_Drive_Belt,
            Elevator_Cross_Shaft,
            Grain_Elev_Top_Shaft,
            Bubble_Up,
            Cleaning_Belt_Drive,
            Tailings_Cross_Auger_Rethresher,
            Tailing_Gearbox,
            Tailings_Incline_Auger,
            Eccentric,
            Main_Clean_Grain_Cross_Auger,
            Auger_Belt_Drive,
            XA_Clean_Grain_Cross_Auger,
            Feeder_RPM,
            Rotor_RPM,
            Clutch_RPM,
            Feeder_Header_Gbx,
            Fdr_JackShaft,
            Feeder_Top_Shaft,
        ]

        self.write_speed()
