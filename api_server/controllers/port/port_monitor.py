from threading import Thread
from controllers.reactor.reactor_controller import ReactorController
from controllers.port.port import Port

class PortMonitor(Thread):
    '''
    Base class for input and output ports for 
    GPIO, MCP3008 and other related devices
    '''
    
    reactor_controller=ReactorController.Instance()
    
    attached_port=None

    def __init__(self,port:Port):
        super(PortMonitor,self).__init__()
        self.attached_port=port
        #print("***** Port Monitor Created {}".format(self.ident))   
        
    def run(self):
        pass


        
