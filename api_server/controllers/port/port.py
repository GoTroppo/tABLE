#from threading import Thread
#from controllers.reactor.reactor_controller import ReactorController

#class Port(Thread):
class Port():
    '''
    Base class for input and output ports for 
    GPIO, MCP3008 and other related devices
    '''
    
    # defaul type of port is input
    is_input=True  
    
    # Holds the current ReactorController
    #reactor_controller = None
    
    def __init__(self):
        #super().__init__(self)
        #print("***** Port Created {}".format(self.ident))
        #print("***** Port Created {}".format(self))
        pass