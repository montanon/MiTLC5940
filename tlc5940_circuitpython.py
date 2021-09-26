import board
from digitalio import DigitalInOut, DriveMode
import busio

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

        self.SPI = busio.SPI(board.D11, board.D10)
        #self.SPI.configure(baudrate=30000, polarity=0, phase=0, bits=8) # TODO: Review setup

        self.BLANK = DigitalInOut(board.D5)
        self.BLANK.switch_to_output(value=1, drive_mode=DriveMode.PUSH_PULL)

        self.n_chips = n_chips



if __name__ == '__main__':

    TLC5940(0, 0)
