class SPN_value_conversion:
    """
    This class is used to convert value provided by pytest to a value that the actual hardware can understand.
    Here the voltage conversion function needs to be added so that for each voltage variation,
    we can add the function according to the voltage received that will convert it to required pot value.
    """

    def __init__(self, ob):
        self._gb = ob
        self.flag_state = 1

    def volt_to_pot(self, volt):  ##10.432V max
        pot_value = round((volt / 1000) * 213 / 10.432)
        return pot_value

    def convert_value(self, spn, value):
        if spn == 542:  # Operator Seat
            if value == 4000:  # Not Seated
                data = 1
            elif value == 8000:  # Seated
                data = 0
        elif spn == 576:  # Rear Ladder
            if value == 2500:  # Ladder Down
                data = 1
            elif value == 7000:  # Ladder Up
                data = 0
        elif spn == 335:
            if value == 2500:
                data = 135
            elif value == 700:
                data = 34
        elif spn == 518:  # Estop
            data = self.volt_to_pot(value)
        elif spn == 66:
            if value == 12000:
                self._gb.feeder_engage_state = 1
                data = 0
            elif value == 0:
                self._gb.feeder_engage_state = 0
                data = 1
        elif spn == 322:
            if value == 12000:
                self._gb.thresher_engage_state = 1
                data = 0
            elif value == 0:
                self._gb.thresher_engage_state = 0
                data = 1

        return data
