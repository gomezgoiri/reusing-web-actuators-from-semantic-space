'''
Created on Sep 20, 2013

@author: tulvur
'''

from actuation.api.lamp_rest import RESTProvider, LampConsumerREST
from actuation.proofs.preprocess import Preprocessor
from actuation.proofs.plan import LemmaPrecedencesGraph
from actuation.proofs.parsers.lemmas import LemmasParser

class LampConsumerRESTMock(LampConsumerREST):
    
    def __init__(self, input_folder, output_folder, reasoner):
        super(LampConsumerRESTMock,self).__init__()
        self.preference_file = input_folder + "additional_info.n3"
        self.output_folder = output_folder
        self.reasoner = reasoner
        
        self._nodes = []
        self.descriptions = set()
        self.base_knowledge = set()
    
    # In the mock implementation, the resources are not retrieved through HTTP
    def discover(self, node):
        self._nodes.append( node )  
    
    def _obtain_resource_descriptions(self):
        for node in self._nodes:
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'options'): # maybe it does not implement it
                        opts = resource.options()
                        if hasattr(opts, '__iter__'):
                            self.descriptions.update( opts ) # == extend in lists
                        else:
                            self.descriptions.add( opts ) # == append in lists
     
    def _obtain_base_knowledge(self):
        '''Crawling to obtain base knowledge (done by an spider, autonomous agent)'''
        for node in self._nodes:
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'get'): # maybe it does not implement it
                        opts = resource.get()
                        self.base_knowledge.add( opts ) # == append in lists
        self.base_knowledge.add( self.preference_file )
    
    def start(self):
        self._obtain_resource_descriptions()
        self._obtain_base_knowledge()
    
    def stop(self):
        pass
    
    def achieve_goal(self, query_goal_path):
        plan_filepath = self._create_plan(query_goal_path, self.descriptions.union( self.base_knowledge ) )
        lgraph = self._process_plan( plan_filepath )
        self._follow_plan( lgraph )
        
    def _create_plan(self, query_goal_path, rule_paths):
        output_file_path = self.reasoner.query_proofs( rule_paths ,
                                                 query_goal_path,
                                                 self.output_folder + "plan.n3" ) # Write the plan into a file
        return output_file_path

    def _process_plan(self, plan_filepath):
        Preprocessor.preprocess( plan_filepath, self.output_folder, self.reasoner )
        lemmas = LemmasParser.parse_file( self.output_folder + Preprocessor.get_output_filename("services"),
                                          self.output_folder + Preprocessor.get_output_filename("bindings"),
                                          self.output_folder + Preprocessor.get_output_filename("evidences") )
        
        lemma_graph = LemmaPrecedencesGraph( self.output_folder + Preprocessor.get_output_filename("precedences"),
                                             lemmas )
        
        #lemma_graph.to_image( output_file = self.output_folder + "lemma_precedences.png" )
        #lemma_graph.to_gml( output_file = self.output_folder + "lemma_precedences.gml" )
        return lemma_graph
    
    def _follow_plan(self, lgraph):
        for n in lgraph.get_shortest_path():
            print n