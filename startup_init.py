# class start_init:
#     global _stg, _sti

#     def __init__(self, ob1, ob2):
#         self._stg = ob1
#         self._sti = ob2

#     def init_key(self):
#         self._sti.key_switch(self._stg.KeyIsON)

#     def init_freq(self):
#         for i in self._stg.fq_ip_spn:
#             self._sti.data_to_board(i, 200)

#     def init_spn(self):
#         self._sti.data_to_board(288, 35)
#         self._sti.data_to_board(314, 45)
#         self._sti.data_to_board(317, 125)
#         self._sti.data_to_board(335, 135)
#         self._sti.data_to_board(339, 80)
#         self._sti.data_to_board(543, 125)
#         self._sti.data_to_board(551, 125)
#         self._sti.data_to_board(583, 35)
#         self._sti.data_to_board(584, 45)

#     def init_volt(self):
#         for i in self._stg.vol_ip_spn:
#             self._sti.data_to_board(i, self._stg.volt_scale_default_dict[i])
