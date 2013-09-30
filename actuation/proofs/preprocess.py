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

from os import path
from optparse import OptionParser


class Preprocessor(object):
    '''
    This class acts as an entry point to generate the processed files from pre-proofs.
    
    These temporary files are generated simply because they are easier to parse.
    '''
        
    EXTRACTIONS = {# identifier: (input_filename, output_filename)
                   "precedences": ("lemma_precedences.n3", "precedences.txt"),
                   "bindings": ("rest_bindings.n3", "bindings.txt"),
                   "services": ("rest_services.n3", "services.txt"),
                   "evidences": ("non_lemma_evidences.n3", "evidences.txt"),
                   }
    
    PATH_TO_GOALS = path.dirname(__file__) + "/goal_rules/"
    
    @staticmethod
    def get_output_filename(identifier):
        return Preprocessor.EXTRACTIONS[identifier][1]
    
    @staticmethod
    def preprocess(input_file, output_folder, reasoner):
        '''
        This method generates the simplified files which will be parsed afterwards.
        '''
        path_to_goals = path.dirname(__file__) + "/goal_rules/"
        
        for input_filename, output_filename in Preprocessor.EXTRACTIONS.itervalues():
            # extract item
            print "Processing %s > %s" % (path_to_goals + input_filename, output_folder + output_filename)
            reasoner.query( input_file,
                            path_to_goals + input_filename,
                            output_folder + output_filename )



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    (options, args) = parser.parse_args()

    from actuation.proofs.reason import EulerReasoner
    reasoner = EulerReasoner( options.euler )
    
    Preprocessor.preprocess(options.input, options.output, reasoner)