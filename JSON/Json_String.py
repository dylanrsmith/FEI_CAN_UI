import json


class UcmJsonClass:
    def __init__(self, cmd, typ, spn, val1, val2, val3):
        self.cmd = cmd
        self.type = typ
        self.spn = spn
        self.val1 = val1
        self.val2 = val2
        self.val3 = val3

    def to_json(self):
        return json.dumps(self.__dict__)
