import sys
sys.path.append('../../fake_rpi')

from fake_rpi import printf
from fake_rpi import toggle_print

# Replace libraries by fake ones
import fake_rpi

sys.modules['RPi'] = fake_rpi.RPi
sys.modules['smbus'] = fake_rpi.smbus
sys.modules['board'] = fake_rpi.board
sys.modules['neopixel'] = fake_rpi.neopixel