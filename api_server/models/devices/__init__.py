
import sys
sys.path.append('../../fake_rpi')

from fake_rpi import printf
from fake_rpi import toggle_print

# Replace libraries by fake ones
import fake_rpi

sys.modules['neopixel'] = fake_rpi.neopixel


__all__ = ["neopixel"]
