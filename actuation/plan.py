'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from tempfile import mkdtemp

from wot2013.tsc.actuation.plan import ActuationPlanCreator
from wot2013.tsc.actuation.preconditions import LemmaPreconditionsChecker
from wot2013.proofs.extract_info import UsefulInformationExtractor
from wot2013.proofs.interpretation.graphs import LemmaPrecedencesGraph
from wot2013.proofs.interpretation.lemma_parser import LemmaParser


class PlanManager(object):
    
    def __init__(self, output_folder, reasoner):
        self.output_folder = mkdtemp( dir = output_folder )
        self.reasoner = reasoner
    
    def create_plan(self, query_goal_path, rule_paths):        
        # Generate plan using fake rules and remove them after getting it
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