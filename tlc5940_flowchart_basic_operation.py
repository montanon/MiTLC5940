import machine
import utime
from machine import Pin

class TLC5940_chip:

    def __init__(self, pins, dc_string, n=1):
        
        self.pins = pins
        
        self.n = n
        self.FirstCycleFlag = 0

        self.VPRG = Pin(self.pins['VPRG'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.DCPRG = Pin(self.pins['DCPRG'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.XLAT = Pin(self.pins['XLAT'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.BLANK = Pin(self.pins['BLANK'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.GSCLK = Pin(self.pins['GSCLK'], Pin.OUT, Pin.PULL_DOWN, value=0)
        
        self.SIN = Pin(self.pins['SIN'], Pin.OUT, Pin.PULL_DOWN, value=0)
        self.SCLK = Pin(self.pins['SCLK'], Pin.OUT, Pin.PULL_DOWN, value=0)
        
        self.LED = Pin(self.pins['LED'], Pin.OUT, Pin.PULL_DOWN, value=0)
        
        self.DotCorrection_setup(dc_string)

        self.chip_setup()

    def chip_setup(self):

        self.GSCLK.value(0)
        self.DCPRG.value(0)
        self.VPRG.value(1)
        self.XLAT.value(0)
        self.BLANK.value(1)

    def DotCorrection_setup(self, dc_string):    

        self.DCPRG.value(1)
        self.VPRG.value(1)
        
        dc_count = 0
        
        while dc_count <= self.n*96 - 1:
            
            bit = int(dc_string[dc_count])
            
            self.SIN.value(bit)
            
            self.SCLK.value(1)
            self.SCLK.value(0)
            
            dc_count += 1
            
        self.LED.value(1)

        self.XLAT.value(1)
        self.XLAT.value(0)
        
        print('Did DC!')
        
        self.LED.value(0)

    def GrayScale_cycle(self, gs_string):
        
        #start = utime.time_ns()

        if self.VPRG.value() == 1:
            self.VPRG.value(0)
            self.FirstCycleFlag = 1

        self.BLANK.value(0)
        
        gs_count = 0
        data_count = 0

        while gs_count <= 4095:
            
            while data_count <= self.n*192 - 1:
                
                bit = int(gs_string[data_count])
                
                self.SIN.value(bit)
                
                self.SCLK.value(1)
                
                data_count += 1
                
                self.SCLK.value(0)
                
            self.GSCLK.value(1)
            
            gs_count += 1
            
            self.GSCLK.value(0)
            
        self.LED.value(1)

        self.BLANK.value(1)

        self.XLAT.value(1)
        self.XLAT.value(0)

        if self.FirstCycleFlag == 1:

            self.SCLK.value(1)
            self.SCLK.value(0)

        self.FirstCycleFlag = 0
        
        #print('Started at = ', start, ' Cycle took = ', utime.time_ns() - start, ' ns')
        
        self.LED.value(0)

if __name__ == '__main__':

    pins = {
            'VPRG': 16,
            'XLAT': 17,
            'SIN': 15,
            'SCLK': 14,
            'SOUT': 0,
            'BLANK': 13,
            'GSCLK': 12,
            'DCPRG': 18,
            'LED': 25
            }
    
    dc_byte_string = '1'*6*16
    
    print('Going')
    
    tlc = TLC5940_chip(pins, dc_byte_string)

    while True:

        gs_byte_string = '111111111111'*1 + '000000000000'*15

        tlc.GrayScale_cycle(gs_byte_string)

        gs_byte_string = '000000000000'*1 + '1000000000000'*1 + '000000000000'*14

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*2 + '111111111111'*1 + '000000000000'*13

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*3 + '1000000000000'*1 + '000000000000'*12

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*4 + '111111111111'*1 + '000000000000'*11

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*5 + '1000000000000'*1 + '000000000000'*10

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*6 + '111111111111'*1 + '000000000000'*9

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*7 + '1000000000000'*1 + '000000000000'*8

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*8 + '111111111111'*1 + '000000000000'*7

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*9 + '1000000000000'*1 + '000000000000'*6

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*10 + '111111111111'*1 + '000000000000'*5

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*11 + '1000000000000'*1 + '000000000000'*4

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*12 + '111111111111'*1 + '000000000000'*3

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*13 + '1000000000000'*1 + '000000000000'*2

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*14 + '111111111111'*1 + '000000000000'*1

        tlc.GrayScale_cycle(gs_byte_string)
        
        gs_byte_string = '000000000000'*15 + '1000000000000'*1

        tlc.GrayScale_cycle(gs_byte_string)