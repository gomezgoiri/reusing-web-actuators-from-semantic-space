# -*- coding: utf-8 -*-
'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
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