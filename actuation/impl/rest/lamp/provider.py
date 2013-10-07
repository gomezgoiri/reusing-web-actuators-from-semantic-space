'''
Created on Sep 19, 2013

@author: tulvur
'''

from actuation.api.rest import RESTProvider
from actuation.impl.rest.lamp.resources import LampResource, LightResource


class LampProviderRESTMock(RESTProvider):
    
    def __init__(self, input_folder, output_folder):
        super(LampProviderRESTMock,self).__init__()
        self.resources['lamp'] = LampResource( input_folder )
        light_resource = LightResource( input_folder,
                                        output_folder )
        self.resources['lamp'].add_sub_resource("actuators/light", light_resource)
    
    def start(self):
        pass
    
    def stop(self):
        pass