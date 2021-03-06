class Reactor():
    '''Base class for Reactors
    '''
    
    # Raspberry Pi ports associated which will react upon trigger
    rpi_ports={}
    
    def __init__(self):
        pass
    
    def addRpiPort(self,rpi_port_id:int,reactor_obj=None):
        self.rpi_ports[rpi_port_id]=reactor_obj
        
    def setRpiPort(self,rpi_port_id:int,reactor_obj):
        self.rpi_ports[rpi_port_id]=reactor_obj
    
    def trigger(self,input_port_data):
        '''This method is used to define the triggers 
        of data from input_port_data
        '''
        pass