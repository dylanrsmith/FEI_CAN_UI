import spidev
import RPi.GPIO as GPIO
import time
import smbus


class HwConnect:
    """
    Module used for communicating to Pi peripheral Boards.

    Using SPI and I2C interfaces.
    """

    i2cbusRack1 = 1  # smbus.SMBus(11)
    i2cbusRack2 = 1  # smbus.SMBus(12)
    i2cbusRack3 = 1  # smbus.SMBus(13)

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    spi = spidev.SpiDev()

    # A0
    GPIO.setup(4, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(0.10)

    # A1
    GPIO.setup(23, GPIO.OUT, initial=GPIO.LOW)

    # A2
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)

    # A3
    GPIO.setup(22, GPIO.OUT, initial=GPIO.LOW)

    def writepotmeter_fn(self, UCMnr, busnr, ic, potmeter, value):
        """

        :param UCMnr:
        :param busnr:
        :param ic:
        :param potmeter:
        :param value:
        """
        GPIO.output(4, (ic - 1) & 0x01)
        GPIO.output(23, ((ic - 1) & 0x02) >> 1)
        GPIO.output(27, ((ic - 1) & 0x04) >> 2)
        GPIO.output(22, ((ic - 1) & 0x08) >> 3)

        # GPIO.output(4, GPIO.LOW)0x18FFC000
        # GPIO.output(23, GPIO.LOW)
        # GPIO.output(27, GPIO.LOW)
        # GPIO.output(22, GPIO.LOW)
        # print ('output IC 1 set')

        if UCMnr == 1:
            if busnr == 0:
                # open (bus, device), opening /dev/spidev<bus>.<device>
                self.spi.open(0, 0)
                self.spi.max_speed_hz = 1000000
                # print ('spi 0, 0 opened')
                self.spi.writebytes([potmeter, value])
                self.spi.close()
                # print ('spi 0, 0 closed')
            if busnr == 1:
                self.spi.open(0, 1)
                self.spi.max_speed_hz = 1000000
                # print ('spi 0, 1 opened')
                self.spi.writebytes([potmeter, value])
                self.spi.close()
                # print ('spi 0, 1 closed')
        if UCMnr == 2:
            if busnr == 0:
                self.spi.open(1, 0)
                self.spi.max_speed_hz = 1000000
                # print ('spi 1, 0 opened')
                self.spi.writebytes([potmeter, value])
                self.spi.close()
                # print ('spi 1, 0 closed')
            if busnr == 1:
                self.spi.open(1, 1)
                self.spi.max_speed_hz = 1000000
                # print ('spi 1, 1 opened')
                self.spi.writebytes([potmeter, value])
                self.spi.close()
                # print ('spi 1, 1 closed')
        if UCMnr == 3:
            if busnr == 0:
                self.spi.open(1, 2)
                self.spi.max_speed_hz = 1000000
                # print ('spi 1, 2 opened')
                self.spi.writebytes([potmeter, value])
                self.spi.close()
                # print ('spi 1, 2 closed')
        # if (UCMnr == 1 and busnr == 1 and ic == 1 and potmeter == 3):
        #    print("Rotor RPM SPN = 347")
        #    time.sleep(0.5)

    def analogInput_fn(self, Racknr, channel, ADCnr):
        """

        :param Racknr:
        :param channel:
        :param ADCnr:
        :return:
        """
        GPIO.output(4, (ADCnr - 1) & 0x01)
        GPIO.output(23, ((ADCnr - 1) & 0x02) >> 1)
        GPIO.output(27, ((ADCnr - 1) & 0x04) >> 2)
        GPIO.output(22, ((ADCnr - 1) & 0x08) >> 3)
        if Racknr == 1:
            self.spi.open(0, 0)
            self.spi.max_speed_hz = 1000000
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            self.spi.close()
            data = ((adc[1] & 3) << 8) + adc[2]
            return data
        if Racknr == 2:
            self.spi.open(1, 0)
            self.spi.max_speed_hz = 1000000
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            self.spi.close()
            data = ((adc[1] & 3) << 8) + adc[2]
            return data
        if Racknr == 3:
            self.spi.open(1, 2)
            self.spi.max_speed_hz = 1000000
            adc = self.spi.xfer2([1, (8 + channel) << 4, 0])
            self.spi.close()
            data = ((adc[1] & 3) << 8) + adc[2]
            return data

    def writei2cbus2bytes_fn(self, Racknr, address, value1, value2):
        """

        :param Racknr:
        :param address:
        :param value1:
        :param value2:
        """

        if Racknr == 1:
            self.i2cbusRack1.write_word_data(address, value1, value2)
        if Racknr == 2:
            self.i2cbusRack2.write_word_data(address, value1, value2)
        if Racknr == 3:
            self.i2cbusRack3.write_word_data(address, value1, value2)

    def readi2cbus2bytes_fn(self, Racknr, address):
        """

        :param Racknr:
        :param address:
        :return:
        """
        # xored with 0xFFFF to invert the LSDs as they are inverted logic
        if Racknr == 1:
            return self.i2cbusRack1.read_word_data(address, 1) ^ 0xFFFF
        if Racknr == 2:
            return self.i2cbusRack2.read_word_data(address, 1) ^ 0xFFFF
        if Racknr == 3:
            return self.i2cbusRack3.read_word_data(address, 1) ^ 0xFFFF
