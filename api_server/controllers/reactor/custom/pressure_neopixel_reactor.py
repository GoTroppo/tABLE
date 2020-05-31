from controllers.reactor.reactor import Reactor
from models.devices.neopixel import Neopixel
from controllers.gpio.gpio_controller import GpioController


class PressureNeopixelReactor(Reactor):
    '''Reactor for XC-3738 pressure sensor triggering
    '''

    def __init__(self):
        super(PressureNeopixelReactor,self).__init__()
        print("***** Created PressureNeopixelReactor")
    
    def trigger(self,data):
        for gpio_id in self.rpi_ports:
            device = None
            if(gpio_id in self.rpi_ports):
                if(self.rpi_ports[gpio_id] is None):
                    device = GpioController.Instance().getAttachedDevice(gpio_id)
                    self.rpi_ports[gpio_id] = device

                device = self.rpi_ports[gpio_id]
                if(device is not None):
                    if(isinstance(device,Neopixel)):
                        if(data > 100):
                            num_pixels=round(data/100)
                            device.rainbow_meter(num_pixels)
                        else:
                            device.blank_neopixel()