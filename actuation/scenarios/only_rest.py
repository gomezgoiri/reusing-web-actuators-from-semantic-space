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

from actuation.proofs.reason import EyeReasoner
from actuation.scenarios.abstract import AbstractSimulation, main
from actuation.impl.rest.lamp.provider import LampProviderRESTMock
from actuation.impl.rest.lamp.consumer import LampConsumerRESTMock
from actuation.impl.rest.mock.discovery import MockDiscovery


class OnlyRESTDevicesSimulator(AbstractSimulation):
    
    def __init__(self, input_folder, output_folder, path_to_reasoner, num_providers, debug = False):
        super(OnlyRESTDevicesSimulator, self).__init__( output_folder )
        self.input_folder = input_folder
        self.reasoner = EyeReasoner( path_to_reasoner )
        self.number_of_providers = num_providers
        self._debug = debug
    
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
        discovery = MockDiscovery()
        self.lp = LampProviderRESTMock( self.input_folder, self.output_folder)
        self.lc = LampConsumerRESTMock( self.input_folder, self.output_folder, self.reasoner, discovery )
        discovery.add_discovered( self.lp, "example.org")
        #print self.lp.get_resource("/lamp/light").get()
    
    def add_more_knowledge_discovered_data(self):
        outc = self._create_benchmarking_content( self.input_folder + "eval/additional.n3.tpl", self.number_of_providers-1 )
        if outc is not None:
            self.lc._uncrawled_kb.add( self._create_benchmarking_file(outc) )
    
    def execute(self):
        '''
        Executes the scenario where the consumer tries to change the light in the environment.
        '''
        # In theory, this should be add during the crawling process (triggered by the provider.start() method).
        # In reality, as we only need it for the performance evaluation, we directly add it here (which is faster and has the same effects :-D).
        self.add_more_knowledge_discovered_data()
        
        # we could make this goal a template also
        self.lc.achieve_goal( self.input_folder + "light_goal.n3" )
    
    def check(self):
        rsc = self.lp.get_resource("/lamp/actuators/light/2/")
        # TODO check that the value of this resource is the desired one (manually checked) 
        return rsc is not None


if __name__ == '__main__':
    main( OnlyRESTDevicesSimulator )