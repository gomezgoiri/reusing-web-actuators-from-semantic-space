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
from actuation.proofs import Binding
from rdflib import Graph
from actuation.proofs import Namespaces



class BindingsParser(object):   
    
    def __init__(self, bindings_path):        
        self.bindings_by_lemma = {}
        self._process_bindings( bindings_path )
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma,_,binding  in rdf_graph.triples((None, Namespaces.REASON.binding, None)):
            lemma_id = str(lemma)
            
            if lemma_id not in self.bindings_by_lemma:
                self.bindings_by_lemma[lemma_id] = []
            
            var = rdf_graph.objects(binding, Namespaces.REASON.var).next()
            bound = rdf_graph.objects(binding, Namespaces.REASON.bound).next()
                
            if var is None or bound is None:
                print "Warning: no 'var' or 'bound' for the binding of lemma %s"%(lemma)
            else:
                self.bindings_by_lemma[lemma_id].append( Binding(var, bound) )



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/bindings.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = BindingsParser( options.input )
    print rsp.bindings_by_lemma