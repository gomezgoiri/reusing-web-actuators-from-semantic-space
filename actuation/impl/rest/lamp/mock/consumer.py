'''
Created on Sep 20, 2013

@author: tulvur
'''

from actuation.api import Node
from actuation.impl.rest.lamp.mock.agents import Crawler, PlanAchiever
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