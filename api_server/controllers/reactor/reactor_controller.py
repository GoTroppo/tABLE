#from controllers.port.port import Port 
#import threading

from controllers.reactor.reactor import Reactor
from controllers.reactor.custom import * 

class ReactorController():
    reactor_input_map = {}

    __instance = None
    @staticmethod 
    def Instance():
        """ Static access method. """
        if ReactorController.__instance == None:
            ReactorController()
            print("***** Created ReactorController")
        return ReactorController.__instance
    
    def __init__(self):
        if ReactorController.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ReactorController.__instance = self
            
    def trigger(self,port,data):
        for my_port in self.reactor_input_map:
            if(my_port.name == port.attached_port.name):
                self.reactor_input_map[my_port].trigger(data)
    
    @staticmethod
    def factory(classname):
        cls = globals()[classname]
        return cls()
    
    def addReactor(self,port_obj,reactor_class_str:str,reactor_port_id:int):
        # First create the Reactor class instance
        if(port_obj not in self.reactor_input_map):
            reactor=ReactorController.factory(reactor_class_str)
            reactor.addRpiPort(reactor_port_id,None)
            self.reactor_input_map[port_obj] = reactor
        else:   # we have an existing port_obj
            if(isinstance(self.reactor_input_map[port_obj],reactor_class_str)):
                self.reactor_input_map[port_obj].addRpiPort(reactor_port_id,None)
            else:
                reactor=ReactorController.factory(reactor_class_str)
                reactor.addRpiPort(reactor_port_id,None)
                self.reactor_input_map[port_obj] = reactor

        print("***** addReactor for port {} Reactor {} attached to {}".format(port_obj.name,reactor,reactor_port_id))
            
