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

import re
from StringIO import StringIO
from os import path
from optparse import OptionParser
from rdflib import Graph
from actuation.proofs import Namespaces


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
    def _fix_the_serialized_mess( n3_serialization_prefixes_everywhere ):
        by_lines = n3_serialization_prefixes_everywhere.split('\n')
        
        prefexp = re.compile(r"@prefix( \w*): <(.+)>\s*.")
        pretty_n3_serialization = ""
        prefixes = set()
        for line in by_lines:
            ls = line.lstrip()
            if ls.startswith("@prefix"):
                for p in prefexp.findall( ls ):
                    prefixes.add( p )
            else:
                indx = ls.find("@prefix") # quick and dirty => if it is inside a string, bad luck :-P
                if indx != -1:
                    ls = ls[:indx] # supress the last part
                pretty_n3_serialization += ls + "\n"
        
        pretty_n3_serialization = "\n\n" + pretty_n3_serialization
        
        for p in prefixes:
            pretty_n3_serialization = "@prefix%s: <%s> .\n" % (p[0], p[1]) + pretty_n3_serialization;
        
        return pretty_n3_serialization
    
    @staticmethod
    # http://answers.semanticweb.com/questions/8336/what-is-skolemization
    def _skolemize_lemmas_and_write_less_optimum(input_file, output_folder):
        filename = output_folder + "skolemized_plan.n3"
        g = Graph()
        g.parse( input_file, format="n3" )
        g2 = g.skolemize() # str(Namespaces.FAKE) )
        # In 4.0.1 this throws an error: https://github.com/RDFLib/rdflib/commit/f5da2a2aca054748877aa7c6d722dc087472a858
        # Until a new version is uploaded: pip install https://github.com/RDFLib/rdflib/tarball/master
        #g2.serialize( filename+".bak", format="n3" ) # awful serialization!
        #print g2.serialize( format="n3")
        prefixes_everywhere = g2.serialize( format="n3" ) # awful serialization!
        serial = Preprocessor._fix_the_serialized_mess( prefixes_everywhere )
        with open (filename, "w") as output_file:
            output_file.write( serial )
        
        return filename
    
    @staticmethod
    # Or much more straight and fast alternative... :-S
    def _skolemize_lemmas_and_write(input_file, output_folder):
        filename = output_folder + "partially_skolemized_plan.n3"
        
        fake_prefix = r"@prefix fake: <%s>." % Namespaces.FAKE
        with open (input_file, "r") as input_file:
            data = re.sub('_:lemma(?P<num>\d+)', 'fake:lemma\g<num>', input_file.read())
            g = Graph()
            g.parse( StringIO( fake_prefix + "\n" + data ), format="n3" )
            with open (filename, "w") as output_file:
                output_file.write( fake_prefix + "\n" + data)
        
        return filename
    
    @staticmethod
    def preprocess(input_file, output_folder, reasoner):
        '''
        This method generates the simplified files which will be parsed afterwards.
        '''
        path_to_goals = path.dirname(__file__) + "/goal_rules/"
        
        skolemized_file = Preprocessor._skolemize_lemmas_and_write( input_file, output_folder )
        
        for input_filename, output_filename in Preprocessor.EXTRACTIONS.itervalues():
            # extract item
            print "Processing %s > %s" % (path_to_goals + input_filename, output_folder + output_filename)
            reasoner.query( skolemized_file,
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