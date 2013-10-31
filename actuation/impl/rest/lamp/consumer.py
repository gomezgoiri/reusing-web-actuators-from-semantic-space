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

from actuation.api import Node
from actuation.impl.rest.mock.agents import Crawler, PlanAchiever
from actuation.proofs.plan import LemmaGraphFactory


class LampConsumerRESTMock(Node):
    
    def __init__(self, input_folder, output_folder, reasoner, discovery):
        super(LampConsumerRESTMock,self).__init__()
        self._discovery = discovery
        self._uncrawled_kb = input_folder + "additional_info.n3"
        
        self.crawler = Crawler( discovery )
        self.lgraph_factory = LemmaGraphFactory( output_folder, reasoner )
    
    def start(self):
        self.crawler.update()
    
    def stop(self):
        pass
    
    def achieve_goal(self, query_goal_path):
        all_knowledge = self.crawler.descriptions.union( self.crawler.base_knowledge )
        all_knowledge.add( self._uncrawled_kb )
        
        lgraph = self.lgraph_factory.create(query_goal_path, all_knowledge)
        pa = PlanAchiever( lgraph, self._discovery )
        pa.achieve()