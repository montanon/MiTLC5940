import board
from digitalio import DigitalInOut, DriveMode, Direction, Pull
import busio
import time
from threading import Thread

import array
import pulseio

from timeit import default_timer as timer

class TLC5940:

    def __init__(self, pins_dict, dc_correction, n_chips=1, config=None):

        self._blank = board.D13
        self._sclk = board.D11
        self._vprg = board.D16
        self._gsclk = board.D12
        self._sin = board.D10
        self._xlat = board.D17
        self._dcprg = board.D18
        self._led = board.D23
        self._cs = board.D26

        self.frequency = 1e7
        self.baudrate = 1e7

        self.pins = pins_dict

        self.SPI = self.set_spi()

        self.BLANK = DigitalInOut(self._blank)
        self.BLANK.direction = Direction.OUTPUT
        self.BLANK.value = True

        self.VPRG = DigitalInOut(self._vprg)
        self.VPRG.direction = Direction.OUTPUT

        self.DCPRG = DigitalInOut(self._dcprg)
        self.DCPRG.direction = Direction.OUTPUT

        self.XLAT = DigitalInOut(self._xlat)
        self.XLAT.direction = Direction.OUTPUT

        self.GSCLK = pulseio.PWMOut(self._gsclk, frequency=self.frequency, duty_cycle=0) # Max 3e7

        self.LED = DigitalInOut(self._led)
        self.LED.direction = Direction.OUTPUT

        self.CS = DigitalInOut(self._cs)
        self.CS.direction = Direction.OUTPUT
        self.CS.value = True

        self.n_chips = n_chips
        self.pwm_runtime = 4096/self.frequency

        self.set_chip()


    def set_chip(self):

        self.DCPRG.value = False
        self.VPRG.value = True
        self.XLAT.value = False
        self.BLANK.value = True


    def set_spi(self, nbits=8):

        spi = busio.SPI(self._sclk, self._sin)

        while not spi.try_lock():
            pass

        spi.configure(baudrate=self.baudrate, phase=0, polarity=0, bits=nbits)

        return spi


    def send_spi_bytes(self, bytes_list):

        self.CS.value = False

        self.SPI.write(bytes(bytes_list))

        self.CS.value = True


    def pulse_gsclk(self, blink=False):

        start = timer()

        self.GSCLK.duty_cycle = 32768

        while timer() - start < self.pwm_runtime:
            pass

        self.GSCLK.duty_cycle = 0 

        if blink:
            self.pulse_led(secs=0.001)      
        

    def pulse_led(self, secs=0.5):

        self.LED.value = True
        time.sleep(secs)
        self.LED.value = False


    def DotCorrection_setup(self, dc_list, check=False, blink=False):

        _nchannels = 16
        _nbits = 6

        self.SPI = self.set_spi(nbits=6)

        if check:
            assert len(dc_list) == _nchannels, f'{_nchannels} channels must be set'
            assert all([dc <= 0x40 for dc in dc_list]), f'Each channel must be {_nbits}bit'

        self.DCPRG.value = True
        self.VPRG.value = True

        dc_count = 0

        for n in range(_nchannels):

            self.send_spi_bytes(dc_list[n])

        self.SPI = self.set_spi(nbits=8)

        if blink:
            self.pulse_led(secs=0.1)



if __name__ == '__main__':

    try:

        dc_list = [0x40]*16

        print(dc_list)

        chip = TLC5940(0, 0)

        for i in range(1):
            chip.pulse_led()
            time.sleep(0.5)

        start = timer()

        #chip.DotCorrection_setup(dc_list, check=False, blink=False)

        print(f'DotCorrection Took = {timer() - start} [s]')

        while True:
            start = timer()

            chip.pulse_gsclk()

            print(f'GrayScaleClock Took = {timer() - start} [s]')


    except KeyboardInterrupt:

        del chip
