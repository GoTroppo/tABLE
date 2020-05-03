import sys
sys.path.append('../../fake_rpi')

from fake_rpi import printf
from fake_rpi import toggle_print

# Replace libraries by fake ones
import fake_rpi

sys.modules['spidev'] = fake_rpi.spidev

__all__ = ["mcp3008_controller"]