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

from rdflib import BNode, RDF
from actuation.proofs import Namespaces, Lemmas, Lemma, Binding, RESTCall


# This can be interesting: https://github.com/RDFLib/rdflib/blob/master/docs/persisting_n3_terms.rst

class LemmasParser(object):
    """
    This class parses what a lemma contains or may contain:
      * evidence template patterns
      * bindings
      * rest services
    """
    
    def __init__(self, graph_to_parse):
        self.rdf_graph = graph_to_parse
    
    def parse(self):
        lemmas = Lemmas() # after the refactoring: is it really necessary?
        
        for lemma,_,_  in self.rdf_graph.triples((None, RDF.type, Namespaces.REASON.Inference)):
            evidences = self._parse_lemma_evidences(lemma)            
            bindings = self._parse_bindings(lemma)
            rest = self._parse_rest_services(lemma)
            lemmas.add( lemma, Lemma(rest, bindings, evidences) ) # rest might be None
        
        return lemmas
    
    #===========================================================================
    # ?lemma a r:Inference ;
    #   r:evidence ?evidences .
    # ?evidence list:in ?evidences .
    # ?evidence a r:Inference .
    #===========================================================================
    def _parse_lemma_evidences(self, lemma):
        ret = []
        list_bnode = self.rdf_graph.objects( lemma, Namespaces.REASON.evidence ).next()
        
        finished = False
        while not finished:
            list_element = self.rdf_graph.triples( (list_bnode, None, None) )
            for el in list_element:
                if el[1] == RDF.first:
                    # __contains__ is overriden
                    if (el[2], RDF.type, Namespaces.REASON.Inference) in self.rdf_graph:
                        ret.append( el[2] )
                elif el[1] == RDF.rest:
                    if el[2] == RDF.nil:
                        finished = True
                    else:
                        list_bnode = el[2]
        
        return ret
    
    ######################### REST BINDINGS #################################
    
    def _parse_variable(self, binding_bnode):
        # binding-bnode  tuple1 tuple2
        #           v     v  v   v
        # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; ...
        tuple1 = self.rdf_graph.triples((binding_bnode, Namespaces.REASON.variable, None)).next()
        tuple2 = self.rdf_graph.triples((tuple1[2], None, None)).next()
        return tuple2[2]
    
    def _parse_boundTo(self, binding_bnode):
        # binding-bnode     tuple1  tuple2 (bnode uri "http://")
        #           v        v  v    v
        # r:binding [ ...; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
        #
        # binding-bnode     tuple1
        #           v        v  v 
        # r:binding [ ...; r:boundTo 19];
        tuple1 = self.rdf_graph.triples((binding_bnode, Namespaces.REASON.boundTo, None)).next()
        
        if isinstance(tuple1[2], BNode):
            # r:binding [ ...; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
            tuple2 = self.rdf_graph.triples((tuple1[2], None, None)).next()
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
    
    def _parse_bindings(self, lemma_node):
        bindings = []
        # r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; r:boundTo [ n3:uri "http://example.org/lamp/obsv"]];
        for _,_,binding_bnode  in self.rdf_graph.triples((lemma_node, Namespaces.REASON.binding, None)):
            var = self._parse_variable(binding_bnode)
            boundTo = self._parse_boundTo(binding_bnode)
            if boundTo is not None:
                bindings.append( Binding(var, boundTo) )
        return bindings
    
    ########################### REST PARSING ###################################
    
    #===========================================================================
    # ?rule r:gives {
    #   ?expr => ?implication .
    # }.
    #===========================================================================
    def _get_rule_implication(self, rule_bnode):
        quote_graph = self.rdf_graph.triples((rule_bnode, Namespaces.REASON.gives, None)).next()[2]
        return quote_graph.triples((None, Namespaces.LOG.implies, None)).next()[2]

    def _get_rest(self, implication_graph):
        ru = None
        for t in implication_graph.triples((None, Namespaces.HTTP.requestURI, None)):
            request_subject = t[0]
            ru = t[2]
            
            m = None
            for method_name in implication_graph.objects(request_subject, Namespaces.HTTP.methodName):
                m = method_name
                break
            b = None
            for body in implication_graph.objects(request_subject, Namespaces.HTTP.body):
                b = body
                break
            return RESTCall(m, ru, b)
        return None

    #===========================================================================
    # ?lemma a r:Inference ;
    #     r:rule ?rule .
    # ?rule r:gives {
    #   ?expr => ?implication .
    # }.
    # 
    # ?implication log:includes {
    #     ?rest http:requestURI ?request_uri ;
    #           http:methodName ?method ;
    #           http:body ?body .
    # } .
    #===========================================================================
    def _parse_rest_services(self, lemma_node):
        for _,_,rule_bnode  in self.rdf_graph.triples((lemma_node, Namespaces.REASON.rule, None)):
            implication_graph = self._get_rule_implication(rule_bnode)
            return self._get_rest(implication_graph)


if __name__ == '__main__':
    from optparse import OptionParser
    from rdflib import Graph
    
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="/tmp/tmpmBY2j7/partially_skolemized_plan.n3",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rdf_graph = Graph()
    rdf_graph.parse(options.input, format="n3")
    lp = LemmasParser( rdf_graph )
    print lp.parse()