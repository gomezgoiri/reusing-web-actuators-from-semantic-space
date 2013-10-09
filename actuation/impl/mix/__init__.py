'''
Created on Sep 20, 2013

@author: tulvur
'''

from tempfile import mkstemp
from actuation.api import Node
from actuation.api.space import AbstractSubscriptionObserver, AbstractCallback
from actuation.impl.rest.mock.agents import Crawler, PlanAchiever
from actuation.impl.space import SPARQLSubscriptionTemplate
from actuation.proofs.plan import LemmaGraphFactory
from actuation.utils.conversors import QueryLanguageConversor


class IntermediaryAgent(Node, AbstractSubscriptionObserver, AbstractCallback):
    """
    This agent intermediates between the space and the REST approach.
    
    It resides in the same machine as the space.
    """
    
    def __init__(self, space, input_folder, output_folder, reasoner, discovery):
        super(IntermediaryAgent,self).__init__()
        self._goals = []
        self._space = space
        self._discovery = discovery
        self.output_folder = output_folder
        
        self.crawler = Crawler( discovery )
        self.lgraph_factory = LemmaGraphFactory( output_folder, reasoner )
        self._generic_template_for_preference_fp = input_folder + "generic_task_subscription.sparql"
        self._all_kb_fp = self.output_folder + "all_knowledge_base.n3"
    
    
    def notify_subscription(self, template):
        """Intercepts subscription to use it as a goal."""
        # priority for the space-based approach?
        if isinstance(template, SPARQLSubscriptionTemplate): # should it capture all the templates or just a subset?
            self._goals.append( self._write_n3_goal_in_file( template.query ) )
    
    def _write_n3_goal_in_file(self, sparql_query):
        """
        @param sparql_query: Query in SPARQL format. 
        @return: The file created by the method which contains the equivalent N3QL goal.
        """
        pathname = mkstemp( suffix=".n3", prefix="goal_", dir=self.output_folder)[1]
        with open( pathname, "w" ) as goal_file:
            goal_file.write( QueryLanguageConversor.sparql_to_n3ql(sparql_query) )
            return pathname
    
    def start(self):
        self.crawler.update() # TODO when?
        
        with open( self._generic_template_for_preference_fp, "r" ) as subscription_file:
            st = SPARQLSubscriptionTemplate( subscription_file.read() )
            self._space.subscribe( st, self )
            # after subscribing myself, otherwise I get the notification of my own subscription!
            self._space.add_subscription_observer( self )
    
    def stop(self):
        pass
    
    def call(self):
        for query_goal_path in self._goals:
            all_knowledge = set()
            all_knowledge.add( self._space_to_file() )
            all_knowledge = all_knowledge.union( self.crawler.descriptions )
            all_knowledge = all_knowledge.union( self.crawler.base_knowledge )
            
            lgraph = self.lgraph_factory.create(query_goal_path, all_knowledge)
            pa = PlanAchiever( lgraph, self._discovery )
            pa.achieve()
            # TODO write the responses in the space
            #  ( to let the consumer now that the effect has taken place )
    
    def _space_to_file(self):
        """
        @return: A filepath with the whole space serialized.
        """
        # ugly as hell!
        # in the long term, another solution should be found
        self._space._da.get_space(None).graphs.serialize( self._all_kb_fp, format="n3" ) # y que sea lo que dios quiera ;-)
        return self._all_kb_fp