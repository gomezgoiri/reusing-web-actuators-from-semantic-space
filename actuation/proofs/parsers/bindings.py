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
from rdflib import Graph, RDF, BNode
from actuation.proofs import Namespaces


class BindingsParser(object):
    
    def __init__(self, plan_file_path):        
        self.bindings_by_lemma = {}
        self._process_bindings( plan_file_path )
    
    def __extract_element(self, rdf_graph, subject, predicate):
        ret = rdf_graph.objects(subject, predicate).next()
        if ret is None:
            raise Exception( "The object for the predicate '%s' could not be extracted." % (predicate) )
        return ret
    
    def __parse_variable(self, rdf_graph, binding_bnode):
        # binding-bnode  tuple1 tuple2
        #           v     v  v   v
        # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; ...
        tuple1 = rdf_graph.triples((binding_bnode, Namespaces.REASON.variable, None)).next()
        tuple2 = rdf_graph.triples((tuple1[2], None, None)).next()
        return tuple2[2]
        
    def __parse_boundTo(self, rdf_graph, binding_bnode):
        # binding-bnode     tuple1  tuple2 (bnode uri "http://")
        #           v        v  v    v
        # r:binding [ ...; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
        #
        # binding-bnode     tuple1
        #           v        v  v 
        # r:binding [ ...; r:boundTo 19];
        tuple1 = rdf_graph.triples((binding_bnode, Namespaces.REASON.boundTo, None)).next()
        
        if isinstance(tuple1[2], BNode):
            # r:binding [ ...; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
            tuple2 = rdf_graph.triples((tuple1[2], None, None)).next()
            if tuple2[1] == Namespaces.N3.uri:
                # r:binding [ ...; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
                return tuple2[2]
            else:
                #raise Exception( "TODO. Not considered case: %s" % (boundType) )
                # For example:
                # r:binding [ ...; r:boundTo [ a r:Existential; n3:nodeId "_:sk3"]];
                pass
        else:
            # r:binding [ ...; r:boundTo 19];
            return tuple1[2] # a Literal
    
    def _process_bindings(self, plan_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(plan_file_path, format="n3")
        
        for lemma,_,_  in rdf_graph.triples((None, RDF.type, Namespaces.REASON.Inference)):
            lemma_id = str(lemma)
            
            if lemma_id not in self.bindings_by_lemma:
                self.bindings_by_lemma[lemma_id] = []
            
            # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
            for _,_,binding_bnode  in rdf_graph.triples((lemma, Namespaces.REASON.binding, None)):
                var = self.__parse_variable(rdf_graph, binding_bnode)
                boundTo = self.__parse_boundTo(rdf_graph, binding_bnode)
                if boundTo is not None:
                    self.bindings_by_lemma[lemma_id].append( Binding(var, boundTo) )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="/tmp/tmpFj3f6D/partially_skolemized_plan.n3",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = BindingsParser( options.input )
    print rsp.bindings_by_lemma