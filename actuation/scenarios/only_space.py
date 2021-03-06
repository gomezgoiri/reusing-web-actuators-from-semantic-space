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

from rdflib import Literal
from rdflib.plugins.sparql import prepareQuery

from actuation.scenarios.abstract import AbstractSimulation, main
from actuation.impl.space import CoordinationSpace, SPARQLSubscriptionTemplate
from actuation.impl.space.lamp.mock.provider import LampProviderSpaceMock
from actuation.impl.space.lamp.mock.consumer import LampConsumerSpaceMock


class OnlySpaceBasedDevicesSimulator(AbstractSimulation):
    
    def __init__(self, input_folder, output_folder, path_to_reasoner, num_providers, debug = False):
        super(OnlySpaceBasedDevicesSimulator, self).__init__( output_folder )
        self.input_folder = input_folder
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
    
    def _get_subscriptions(self, tpl_fp):
        with open( tpl_fp, "r" ) as subscription_tpl_file:
            return  SPARQLSubscriptionTemplate( subscription_tpl_file.read() )
    
    def add_knowledge_to_space(self):
        # load triples
        graph = self._get_additional_knowledge_graph( self.input_folder + "eval/additional.n3.tpl", self.number_of_providers-1 )
        if graph is not None:
            # I know for sure that no subscription will be activated with this graph,
            # so I've opted for making this loading phase which is not measured quicker...
            self.space.write( graph, ignore_subscriptions = True )
        subscription_for_replicas =  self._get_subscriptions( self.input_folder + "eval/task_subscription.sparql" )
        for _ in range(self.number_of_providers-1):
            self.space.subscribe( subscription_for_replicas , None ) # will not be activated, so callback==None
    
    def configure(self):
        self.space = CoordinationSpace("onlySpace")
        self.add_knowledge_to_space();
        
        self.lp = LampProviderSpaceMock( self.space, self.input_folder, self.output_folder, debug = self._debug )
        self.lc = LampConsumerSpaceMock( self.space, self.input_folder, self.output_folder, debug = self._debug )
    
    def execute(self):
        '''
        Executes the scenario where the consumer tries to change the light in the environment.
        '''
        light_value = 30
        self.lc.subscribe_to_result(light_value)
        self.lc.write_task(light_value)
    
    def check(self):
        # This could be done also by the consumer to check if everything went OK or nothing changed.
        # E.g. it subscribes to that and querying...
        q = """
            prefix : <http://example.org/lamp/>
            prefix sweet:  <http://sweet.jpl.nasa.gov/>
            prefix frap: <http://purl.org/frap/>
            prefix dul:  <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>
            prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
            prefix ucum:  <http://purl.oclc.org/NET/muo/ucum/>
            prefix actuators:  <http://example.org/lamp/actuators/>
        
            construct { <http://whatev/s> <http://whatev/o> ?val } where {
                #actuators:light ssn:madeObservation ?measure .
                ?measure ssn:observationResult ?observationr .
                ?observationr ssn:hasValue ?observationv .
                ?observationv dul:hasDataValue ?val .
            }"""
        val = self.space.query_by_sparql( prepareQuery( q ) )
        l = val.triples((None,None,None)).next()[2]
        #print "%s" % l
        return Literal(30) == l


if __name__ == '__main__':
    main( OnlySpaceBasedDevicesSimulator )