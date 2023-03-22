from IOCtrl import *
import time
import threading
from threading import *


class ReadThread:
    global _re

    highprio_spns = [419, 418, 417, 420, 375, 376, 377]
    highprio_spns_write = [347, 348]

    def __init__(self, ob):
        # print("Read thread started")
        self._re = ob
        # add signals to write initially as in update fn

    def read(self):
        counter = 0
        for i in range(1000):
            counter += 1
            j = i + 1
            self._re.data_from_board(j)
            self._re.data_write_board(j)

            if counter == 20:
                counter = 0
                for k in self.highprio_spns:
                    self._re.data_from_board(k)
                for k in self.highprio_spns_write:
                    self._re.data_write_board(k)
        # write after read
        # self._re.data_write_board_main()
        threading.Timer(0, self.read).start()  # 500 ms read thread second read thread
        # print("Current Thread : ", (threading.current_thread()), "Time : ", (time.time()))
