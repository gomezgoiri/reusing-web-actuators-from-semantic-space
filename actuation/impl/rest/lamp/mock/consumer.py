'''
Created on Sep 20, 2013

@author: tulvur
'''

from actuation.api import Node
from actuation.impl.rest.lamp.mock.agents import Crawler
from actuation.proofs.preprocess import Preprocessor
from actuation.proofs.plan import LemmaPrecedencesGraph
from actuation.proofs.parsers.lemmas import LemmasParser


class LampConsumerRESTMock(Node):
    
    def __init__(self, input_folder, output_folder, reasoner, discovery):
        super(LampConsumerRESTMock,self).__init__()
        self.output_folder = output_folder
        self.reasoner = reasoner
        self.discovery = discovery
        self.crawler = Crawler(input_folder, discovery)
    
    def start(self):
        self.crawler.update()
    
    def stop(self):
        pass
    
    def achieve_goal(self, query_goal_path):
        all_knowledge = self.crawler.descriptions.union( self.crawler.base_knowledge )
        plan_filepath = self._create_plan(query_goal_path, all_knowledge )
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
    
    def __make_call(self, lemma):
        # TODO the output of a call should be parsed: it may be the input of another one
        nret = self.discovery.get_node( lemma.rest.request_uri )
        if nret:
            node, remaining_path = nret
            rsc = node.get_resource( remaining_path )
            
            if rsc is None:
                print "Resource '%s' not found in node." % (remaining_path)
            else:
                met = str(lemma.rest.method)
                if met == "POST":
                    body = lemma.get_binding( lemma.rest.var_body )
                    return rsc.post( body )
                elif met == "GET":
                    return rsc.get()
                else:
                    raise Exception( "TODO, HTTP verb: %s" % (lemma.rest.method) )
        else:
            print "Node not found"
        
    
    def _follow_plan(self, lgraph):
        for n in lgraph.get_shortest_path():
            #print n
            if n.is_rest_call():
                # deliberated ignore of the return
                # in this project we just check a simple path composed by a unique rest call 
                self.__make_call( n )
                