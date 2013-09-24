'''
Created on Sep 20, 2013

@author: tulvur
'''

from actuation.api.lamp_rest import RESTProvider, LampConsumerREST
from actuation.proofs.extract_info import UsefulInformationExtractor
from actuation.proofs.interpretation.graphs import LemmaPrecedencesGraph
from actuation.proofs.interpretation.lemma_parser import LemmaParser

class LampConsumerRESTMock(LampConsumerREST):
    
    def __init__(self, output_folder, reasoner):
        super(LampConsumerRESTMock,self).__init__()
        self._nodes = []
        self.descriptions = []
        self.output_folder = output_folder
        self.reasoner = reasoner
    
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
                            self.descriptions.extend( opts )
                        else:
                            self.descriptions.append( opts )
    
    def start(self):
        self._obtain_resource_descriptions()
    
    def stop(self):
        pass
    
    def achieve_goal(self, query_goal_path):
        plan_filepath = self.create_plan(query_goal_path, self.descriptions)
        
    def create_plan(self, query_goal_path, rule_paths):
        output_file_path = self.reasoner.query_proofs( rule_paths ,
                                                 query_goal_path,
                                                 self.output_folder + "/plan.n3" ) # Write the plan into a file
        return output_file_path

    def process_plan(self):
        uie = UsefulInformationExtractor( self.plan_path, self.output_folder, self.reasoner )
        uie.extract_all()
        
        self.lemma_graph = LemmaPrecedencesGraph(self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("precedences"))
        
        lp = LemmaParser( self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("services"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("bindings"),
                          self.output_folder + "/" + UsefulInformationExtractor.get_output_filename("evidences") )
        self.lemma_graph.add_lemmas_info( lp.lemmas )
        self.lemma_graph.create_nx_graph()
        #self.lemma_graph.to_image( output_file = options.output + "/lemma_precedences.png" )
        #self.lemma_graph.to_gml( output_file = self.output_folder + "/lemma_precedences.gml" )