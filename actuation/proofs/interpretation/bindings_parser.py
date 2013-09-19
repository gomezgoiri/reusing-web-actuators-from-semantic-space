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
from rdflib import Graph, Namespace, URIRef
from actuation.proofs.interpretation.variable import Variable

r_ns = Namespace("http://www.w3.org/2000/10/swap/reason#")


class Binding(object):
    
    def __init__(self, variable, bound):
        self.variable = Variable.create( variable )
        self.bound = bound 
    
    @property
    def bound(self):
        return self._bound
    
    @bound.setter
    def bound(self, bound):
        self._bound = self._get_proper_bound( bound ) # should be URIRef?
    
    def _get_proper_bound(self, bound):
        ret = Variable.create(bound)
        if ret is None:
            if bound.startswith("http://"):
                ret = URIRef( bound )
            else: # TODO literal
                return bound
        return ret
    
    def __eq__(self, other_binding):
        return self.variable == other_binding.variable and self.bound == other_binding.bound

    def __hash__(self):
        return hash(self.variable) + hash(self.bound)
    
    def __repr__(self):
        return "b(var: %s, bound: %s)" % (self.variable, self.bound)


class BindingsParser(object):   
    
    def __init__(self, bindings_path):        
        self.bindings_by_lemma = {}
        self._process_bindings( bindings_path )
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma,_,binding  in rdf_graph.triples((None, r_ns.binding, None)):
            lemma_id = str(lemma)
            
            if lemma_id not in self.bindings_by_lemma:
                self.bindings_by_lemma[lemma_id] = []
            
            var = rdf_graph.objects(binding, r_ns.var).next()
            bound = rdf_graph.objects(binding, r_ns.bound).next()
                
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