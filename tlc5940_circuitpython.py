import board
from digitalio import DigitalInOut, DriveMode, Direction, Pull
import busio
import time

import array
import pulseio

class TLC5940:

    def __init__(self, pins_dict, dc_correction, n_chips=1, config=None):

        _blank = 'BLANK'
        _sckl = 'SCKL'
        _vpgr = 'VPGR'
        _gsclk = 'GSCLK'
        _sin = 'SIN'
        _xlat = 'XLAT'
        _dcprg = 'DCPRG'

        self.pins = pins_dict

        self.SPI = self.set_spi(board.D11, board.D10)

        self.BLANK = DigitalInOut(board.D13)
        self.BLANK.direction = Direction.OUTPUT
        self.BLANK.value = True

        self.VPRG = DigitalInOut(board.D16)
        self.VPRG.direction = Direction.OUTPUT

        self.DCPRG = DigitalInOut(board.D18)
        self.DCPRG.direction = Direction.OUTPUT

        self.XLAT = DigitalInOut(board.D17)
        self.XLAT.direction = Direction.OUTPUT

        self.GSCLK = pulseio.PWMOut(board.D12, frequency=3e7, duty_cycle=32768)

        self.LED = DigitalInOut(board.D23)
        self.LED.direction = Direction.OUTPUT

        self.CS = DigitalInOut(board.D26)
        self.CS.direction = Direction.OUTPUT
        self.CS.value = True

        self.n_chips = n_chips

        self.set_chip()

    def set_chip(self):

        self.DCPRG.value = False
        self.VPRG.value = True
        self.XLAT.value = False
        self.BLANK.value = True

    def set_spi(self, clock, sin):

        spi = busio.SPI(clock, sin)

        while not spi.try_lock():
            pass

        spi.configure(baudrate=int(3e+7), phase=0, polarity=0, bits=8)

        return spi

    def send_spi_bytes(self, bytes_list):

        self.CS.value = False

        self.SPI.write(bytes(bytes_list))

        self.CS.value = True

    def run_gsclk(self, n_pulses=4096):

        gslck = array.array('H', [65000, 1000] * n_pulses * self.n_chips)

        #self.GSCLK.send(gsclk)

    def pulse_led(self, secs=0.5):

        self.LED.value = True
        time.sleep(secs)
        self.LED.value = False

    def DotCorrection_setup(self, dc_list, n_first=2, check=False):

        _nchannels = 16
        _nbits = 6

        if check:
            assert len(dc_list) == _nchannels, f'{_nchannels} channels must be set'
            assert all([dc <= 0x40 for dc in dc_list]), f'Each channel must be {_nbits}bit'

        self.DCPRG.value = True
        self.VPRG.value = True

        dc_count = 0

        for n in range(n_first):

            print(n)

            print(dc_list[n], n)

            self.send_spi_bytes(dc_list[n])

        self.run_gsclk()

        for n in range(_nchannels - n_first):

            print(n)

            print(dc_list[n], n)

            self.send_spi_bytes(dc_list[n_first+n])


if __name__ == '__main__':

    try:

        dc_list = [0x40]*16

        print(dc_list)

        chip = TLC5940(0, 0)

        for i in range(1):
            chip.pulse_led()
            time.sleep(0.5)

        chip.DotCorrection_setup(dc_list, check=True)
        

    except KeyboardInterrupt:

        del chip
