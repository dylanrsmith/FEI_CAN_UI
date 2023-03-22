class gdpb_plant:
    global _gdpb

    def __init__(self, ob1, ob2):
        self._gdpb = ob1
        self._io = ob2
        self.sol_active_flag = 1

    def volt_to_pot(self, vol):
        pot = round((vol / 4.613) * 230)
        return pot

    def calculate(self):
        if self._gdpb.gdpb_enabled == 1:
            if self._gdpb.testing_active == 0:
                self._gdpb.gdpb_disenage_sol = self._io.data_read(
                    654
                )  ## park brake status

            if self._gdpb.gdpb_disenage_sol > 150 and self.sol_active_flag == 1:  ## 50
                self.sol_active_flag = 2
                if self._gdpb.gdpb_link_to_sensor == 1:
                    self._gdpb.gdpb_park_brake_sensor = (
                        2.92  ## Set park brake pressure to 24 PSI
                    )
            elif (
                self._gdpb.gdpb_disenage_sol > 830 and self.sol_active_flag == 2
            ):  ## 350
                self.sol_active_flag = 3
            elif (
                self.sol_active_flag == 3 and self._gdpb.gdpb_disenage_sol < 800
            ):  ## 350
                self.sol_active_flag = 4
                if self._gdpb.gdpb_link_to_sensor == 1:
                    self._gdpb.gdpb_park_brake_sensor = (
                        0.499  ## Set park prake pressure to 0 PSI
                    )
            elif self._gdpb.gdpb_disenage_sol < 150 and self.sol_active_flag == 4:  ##50
                self.sol_active_flag = 1

            if self._gdpb.testing_active == 0:
                self.volt_to_pot_value = self.volt_to_pot(
                    self._gdpb.gdpb_park_brake_sensor
                )  ## COnvert voltage to potmeter val.ue
                self._io.data_to_board(
                    521, self.volt_to_pot_value
                )  ## Park Brake Disengage Sol
                ## Default state to be zero
                self._io.data_to_board(589, 24)  ## RH brake pressure status
                self._io.data_to_board(590, 24)  ## LH brake pressure status
