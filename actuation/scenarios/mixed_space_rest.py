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

from actuation.proofs.reason import EulerReasoner
from actuation.scenarios.abstract import AbstractSimulation, main
from actuation.impl.space import CoordinationSpace
from actuation.impl.rest.lamp.provider import LampProviderRESTMock
from actuation.impl.space.lamp.mock.consumer import LampConsumerSpaceMock
from actuation.impl.mix import IntermediaryAgent
from actuation.impl.rest.mock.discovery import MockDiscovery


class OnlySpaceBasedDevicesSimulator(AbstractSimulation):
    
    def __init__(self, input_folder, output_folder, path_to_reasoner, num_providers, debug = False):
        super(OnlySpaceBasedDevicesSimulator, self).__init__( output_folder )
        self.input_folder = input_folder
        self.reasoner = EulerReasoner( path_to_reasoner )
    
    @property    
    def lc(self):
        return self.nodes["consumer"]
    
    @lc.setter
    def lc(self, value):
        self.nodes["consumer"] = value
    
    @property    
    def lp(self):
        return self.nodes["provider"]
    
    @lp.setter
    def lp(self, value):
        self.nodes["provider"] = value
    
    def configure(self):
        debug = True
        discovery = MockDiscovery()
        
        self.space = CoordinationSpace("mixedSpace")
        self.nodes["agent"] = IntermediaryAgent( self.space,
                                                 self.input_folder+"mix/",
                                                 self.output_folder,
                                                 self.reasoner,
                                                 discovery)
        
        self.lp = LampProviderRESTMock( self.input_folder + "rest/", self.output_folder)
        self.lc = LampConsumerSpaceMock( self.space,
                                         self.input_folder + "space/",
                                         self.output_folder,
                                         debug = debug )
        discovery.add_discovered( self.lp, "example.org")
    
    def execute(self):
        """
        Executes the scenario with a REST provider and a consumer using a space.
        """
        light_value = 30
        self.lc.subscribe_to_result(light_value)
        self.lc.write_task(light_value)
    
    def check(self):
        rsc = self.lp.get_resource("/lamp/actuators/light/2/")
        # TODO check that the value of this resource is the desired one (manually checked) 
        return rsc is not None


if __name__ == '__main__':
    main( OnlySpaceBasedDevicesSimulator )