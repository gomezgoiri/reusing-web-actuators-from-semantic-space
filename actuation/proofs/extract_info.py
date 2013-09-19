'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from os import remove, path
from optparse import OptionParser
from actuation.proofs.goal_rules.query import QueryExecutor
from actuation.proofs.processing.unblank_lemmas import unblank_lemmas

'''
This is the entry point for processing a file with proof results. 
'''
class UsefulInformationExtractor(object):
        
    EXTRACTIONS = {# identifier: (input_filename, output_filename)
                   "precedences": ("lemma_precedences.n3", "precedences.txt"),
                   "bindings": ("rest_bindings.n3", "bindings.txt"),
                   "lemmas": ("lemma_precedences.n3", "lemmas.txt"),
                   "services": ("rest_services.n3", "services.txt"),
                   "evidences": ("non_lemma_evidences.n3", "evidences.txt"),
                   }
    
    def __init__(self, input_file, output_folder, reasoner):
        self.input_file = input_file
        self.output_folder = output_folder
        self.reasoner = reasoner
        self.path_to_goals = path.dirname(__file__) + "/goal_rules"
    
    def start(self):
        self.tmp_file = self.output_folder + "/unblanked.n3"
        unblank_lemmas( self.input_file, self.tmp_file )
        self.default_qe = QueryExecutor( self.tmp_file, self.reasoner )
        
    def stop(self):
        remove( self.tmp_file )
    
    @staticmethod
    def get_input_filename(identifier):
        return UsefulInformationExtractor.EXTRACTIONS[identifier][0]
    
    @staticmethod
    def get_output_filename(identifier):
        return UsefulInformationExtractor.EXTRACTIONS[identifier][1]
    
    def extract_item(self, identifier):
        input_name = UsefulInformationExtractor.get_input_filename(identifier)
        output_name = UsefulInformationExtractor.get_output_filename(identifier)
        self.default_qe.execute_and_save( self.path_to_goals + "/" + input_name,
                                          self.output_folder + "/" + output_name )
    
    def extract_all(self):
        self.start()
        
        #self.extract_item("lemmas") # no longer needed, I think # TODO check
        self.extract_item("precedences")
        self.extract_item("bindings")
        self.extract_item("services")
        self.extract_item("evidences")
        
        self.stop()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()

    from actuation.euler.reasoner import EulerReasoner
    reasoner = EulerReasoner( options.euler )

    uie = UsefulInformationExtractor(options.input, options.output, reasoner)
    uie.extract_all()