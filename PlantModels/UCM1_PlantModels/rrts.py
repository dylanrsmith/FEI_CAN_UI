class rrts_plant:
    global _rrts, _io

    def __init__(self, ob1, ob2):
        self._rrts = ob1
        self._io = ob2

    def calculate(self):
        if self._rrts.agge_enable == 1:
            if self._rrts.testing_active == 0:
                self._rrts.rrts_rocktrap_open = self._io.data_read(
                    140
                )  # Rocktrap Open Sol
                self._rrts.rrts_rocktrap_close = self._io.data_read(
                    143
                )  # Rocktrap Close Sol

            # ~ if self._rrts.testing_active == 0:
            # ~ self._io.data_to_board(1, self.volt_to_pot(self._rrts.rrts_door_closed_state))
