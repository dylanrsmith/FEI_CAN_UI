class lut:
    def __init__(self):
        print(2)

    def get_val(self, list_ip, list_op, val):
        """

        :param list_ip:
        :param list_op:
        :param val:
        :return:
        """
        len_ip = len(list_ip)

        for i in range(len_ip - 1):
            data_prev = list_ip[i]
            data_next = list_ip[i + 1]

            if val > data_prev:
                if val < data_next:
                    val1 = list_op[i]
                    val2 = list_op[i + 1]
                    temp = (val2 - val1) / (data_next - data_prev)
                    new_val = (temp * (val - data_prev)) + val1
                    return abs(new_val)

        return 0
