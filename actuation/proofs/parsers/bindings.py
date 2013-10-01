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
from rdflib import Graph, RDF
from actuation.proofs import Namespaces


# Two examples of the possible shape of a binding:
# + Example 1: ?x0 must be bound to an URI
#     fake:lemma2 r:binding _:sk6.
#     _:sk6 r:var "http://localhost/var#x0".
#     _:sk6 r:boundType n3:uri.
#     _:sk6 r:bound "http://example.org/lamp/obsv".
#     _:sk6 r:bound2 _:e23.
# + Example 2: ?x1 must be bound to a number (19)
#     fake:lemma2 r:binding _:sk7.
#     _:sk7 r:var "http://localhost/var#x1".
#     _:sk7 r:boundType <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>.
#     _:sk7 r:bound e:Numeral.
#     _:sk7 r:bound2 19 .


# Uninteresting cases for us (yet they need to be carefully analyzed):
# + Case 1:
#     fake:lemma1 r:binding _:sk2.
#     _:sk2 r:var "http://localhost/var#x1".
#     _:sk2 r:boundType <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>.
#     _:sk2 r:bound r:Existential.
#     _:sk2 r:bound2 _:e7.
# + Case 2:
#     fake:lemma1 r:binding _:sk3.
#     _:sk3 r:var "http://localhost/var#x1".
#     _:sk3 r:boundType n3:nodeId.
#     _:sk3 r:bound "_:sk3".
#     _:sk3 r:bound2 _:e7.

class BindingsParser(object):
    
    def __init__(self, bindings_path):        
        self.bindings_by_lemma = {}
        self._process_bindings( bindings_path )
    
    def __extract_element(self, rdf_graph, subject, predicate):
        ret = rdf_graph.objects(subject, predicate).next()
        if ret is None:
            raise Exception( "The object for the predicate '%s' could not be extracted." % (predicate) )
        return ret
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma,_,binding  in rdf_graph.triples((None, Namespaces.REASON.binding, None)):
            lemma_id = str(lemma)
            
            if lemma_id not in self.bindings_by_lemma:
                self.bindings_by_lemma[lemma_id] = []
            
            var = self.__extract_element(rdf_graph, binding, Namespaces.REASON.var)
            boundType = self.__extract_element(rdf_graph, binding, Namespaces.REASON.boundType)
            bound = self.__extract_element(rdf_graph, binding, Namespaces.REASON.bound)
            
            if boundType == Namespaces.N3.uri:
                self.bindings_by_lemma[lemma_id].append( Binding(var, bound) )
            
            elif boundType == RDF.type:
                if bound == Namespaces.E.Numeral:
                    number = self.__extract_element(rdf_graph, binding, Namespaces.REASON.bound2)
                    # type(number) is already a Literal
                    self.bindings_by_lemma[lemma_id].append( Binding(var, number) )
                else:
                    #raise Exception( "TODO. Not considered datatype: %s" % (bound) )
                    pass
            else:
                #raise Exception( "TODO. Not considered case: %s" % (boundType) )
                pass



if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/bindings.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = BindingsParser( options.input )
    print rsp.bindings_by_lemma