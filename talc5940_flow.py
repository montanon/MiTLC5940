import machine
import utime
from machine import Pin

class TLC5940_chip:

    def __init__(self, pins, n=1):

        self.VPRG = Pin(pins['VPRG'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.DCPRG = Pin(pins['DCPRG'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.XLAT = Pin(pins['XLAT'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.BLANK = Pin(pins['BLANK'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.GSCLK = Pin(pins['GSCLK'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.SIN = Pin(pins['SIN'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.SCLK = Pin(pins['SCLK'], Pin.OUT, Pin.PULL_DOWN, value=0)

        self.n = n
        self.FirstCycleFlag = 0

        self.chip_setup()

    def chip_setup(self):

        self.GSCLK.value(0)
        self.SCLK.value(0)
        self.DCPRG.value(0)
        self.VPRG.value(1)
        self.XLAT.value(0)
        self.BLANK.value(1)

    def DotCorrection_setup(self, byte_array):    

        self.DCPRG.value(1)
        self.VPRG.value(1)

        dc_count = 0
        
        while dc_count <= self.n*96 - 1:

            bit = int(byte_array[dc_count])

            self.SIN.value(bit)

            self.SCLK.value(1)
            self.SCLK.value(0)

            dc_count += 1

        self.XLAT.value(1)
        self.XLAT.value(0)

    def GrayScale_cycle(self, byte_array):    

        if self.VPRG.value() == 1:
            self.VPRG.value(0)
            self.FirstCycleFlag = 1

        gs_count = 0
        data_count = 0

        self.BLANK.value(0)

        while gs_count <= 4095:
            while data_count <= n*192 - 1:

                bit = int(byte_array[data_count])

                self.SIN.value(bit)

                self.SCLK.value(1)
                self.SCLK.value(0)

                data_count += 1

            self.GSCLK.value(1)
            self.GSCLK.value(0)

            gs_count += 1

        self.BLANK.value(1)

        self.XLAT.value(1)
        self.XLAT.value(0)

        if self.FirstCycleFlag == 1:

            self.SCLK.value(1)
            self.SCLK.value(0)

        self.FirstCycleFlag = 0    

if __name__ == '__main__':

    SCLKf = 30
    GSCLKf = 30
    SCLKp = 16
    GSCLKp = 16
    XLATp = 30
    BLANKp = 20

    tsu0 = 5 #SIN_to_SCLK_high
    tsu1 = 10 #SCLK_low_to XLAT_high
    tsu2 = 10 #VPRG_high_low_to_SCLK_high
    tsu3 = 10 #VPRG_high_low_XLAT_high
    tsu4 = 10 #BLANK_low_to_GSCLK_high
    tsu5 = 30 #XLAT_high_to_GSCLK_high
    tsu6 = 1e6 #VPRG_high_to_DCPRG_high

    th0 = 3 #SCLK_high_to_SIN
    th1 = 10 #XLAT_low_to_SCLK_high
    th2 = 20 #SCLK_high_to_VPRG_high_low
    th3 = 10 #XLAT_low_to_VPRG_high_low
    th4 = 10 #GSCLK_high_to_BLANK_high
    th5 = 1e6 #DCPRG_low_to_VPRG_low

    tr0 = 16
    tr1 = 30

    tf0 = 16
    tf1 = 30
    
    tpd0 = 30
    tpd1 = 60 
    tpd2 = 1000
    tpd3 = 60
    tpd4 = 60
    tpd5 = 30

    td = 30

    n_channels = 16

    channels = {chan : 4096 for chan in range(n_channels)} #4096 led_low, 0 led_high

    pins = {
            'VPRG': 16,
            'XLAT': 17,
            'SIN': 15,
            'SCLK': 14,
            'SOUT': 0,
            'BLANK': 13,
            'GSCLK': 12,
            'DCPRG': 0
            }

    tlc = TLC5940_chip(pins)

    dc_byte_string = '1'*6*16

    tlc.DotCorrection_setup(dc_byte_string)

    while True:

        gs_byte_string = '1'*12*16

        tlc.GrayScale_cycle(gs_byte_string)

        gs_byte_string = '0'*12*16

        tlc.GrayScale_cycle(gs_byte_string)