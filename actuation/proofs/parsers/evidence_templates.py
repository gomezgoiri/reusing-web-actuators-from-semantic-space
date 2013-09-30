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

from optparse import OptionParser
from rdflib import Graph
from actuation.proofs import Template
from actuation.proofs import Namespaces



class EvidenceTemplatesParser(object):   
    
    def __init__(self, bindings_path):        
        self.templates_by_lemma = {}
        self._process_bindings( bindings_path )
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma,_,template  in rdf_graph.triples((None, Namespaces.LOG.includes, None)):
            lemma_id = str(lemma)
            
            for template in template.triples((None, None, None)):
                if lemma_id not in self.templates_by_lemma:
                    self.templates_by_lemma[ lemma_id ] = []
                # there should be just one
                self.templates_by_lemma[ lemma_id ].append( Template( template ) )



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/evidences.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    etp = EvidenceTemplatesParser( options.input )
    print etp.templates_by_lemma