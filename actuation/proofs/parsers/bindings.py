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
from rdflib import BNode
from actuation.proofs import Namespaces


class BindingsParser(object):
    
    def _extract_element(self, rdf_graph, subject, predicate):
        ret = rdf_graph.objects(subject, predicate).next()
        if ret is None:
            raise Exception( "The object for the predicate '%s' could not be extracted." % (predicate) )
        return ret
    
    def _parse_variable(self, rdf_graph, binding_bnode):
        # binding-bnode  tuple1 tuple2
        #           v     v  v   v
        # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; ...
        tuple1 = rdf_graph.triples((binding_bnode, Namespaces.REASON.variable, None)).next()
        tuple2 = rdf_graph.triples((tuple1[2], None, None)).next()
        return tuple2[2]
        
    def _parse_boundTo(self, rdf_graph, binding_bnode):
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
    
    def parse_bindings(self, rdf_graph, lemma_node):
        bindings = []
        # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
        for _,_,binding_bnode  in rdf_graph.triples((lemma_node, Namespaces.REASON.binding, None)):
            var = self._parse_variable(rdf_graph, binding_bnode)
            boundTo = self._parse_boundTo(rdf_graph, binding_bnode)
            if boundTo is not None:
                bindings.append( Binding(var, boundTo) )
        return bindings


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/partially_skolemized_plan.n3",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = BindingsParser( options.input )
    print rsp.bindings_by_lemma