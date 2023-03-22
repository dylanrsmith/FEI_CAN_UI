# from IOCtrl import *
class clrm_plant:
    global _cl, _io
    Engine_RPM = 0
    Low_Idle_Value = 165
    High_Idle_Value = 245
    Engine_Stall_Value = 40  ## 100 --> 40

    def __init__(self, ob1, ob2):
        self._cl = ob1
        self._io = ob2

    def calculate_speed(self):
        self.Engine_RPM = self._cl.current_spd

        if (
            self.Engine_RPM >= 1000
            and self.Engine_RPM < 1450
            and self._cl.Aux_PTO_enabled == 1
        ):
            self._io.data_to_board(91, self.Low_Idle_Value)

        elif (
            self.Engine_RPM > 1450 and self._cl.Aux_PTO_enabled == 1
        ):  # and self.Engine_RPM = 1900:
            self._io.data_to_board(91, self.High_Idle_Value)

        elif self.Engine_RPM == 0 and self._cl.Aux_PTO_enabled == 0:
            self._io.data_to_board(91, self.Engine_Stall_Value)

        elif self._cl.Aux_PTO_enabled == 0:
            self._io.data_to_board(91, self.Engine_Stall_Value)


#         spd_temp = self._cl.sp_val[19]
#
#         prev_output_spd = self._cl.tail_sensor_spd
#
#         if self._cl.clrm_enabled == 1:
#
#             if spd_temp > 0:
#                 spd = (60*1000)/spd_temp
#             else:
#                 spd = 2000
#
#             if self._cl.periodstate == 1:
#                 new_spd = spd - ((self._cl.period*self._cl.degree)/360)
#             else:
#                 new_spd = (spd*self._cl.degree)/360
#             self._cl.periodstate = 1 - self._cl.periodstate #toggle the periods for tb and ts
#             self._cl.tail_sensor_spd = new_spd
#
#         else:
#             self._cl.tail_sensor_spd = prev_output_spd
#        if self._cl.testing_active == 0:
#            self._io.data_to_board(91, self._cl.tail_sensor_spd)
