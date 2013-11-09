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
from actuation.proofs import Namespaces
from actuation.proofs import RESTCall


class RESTServicesParser(object):

    #===========================================================================
    # ?rule r:gives {
    #   ?expr => ?implication .
    # }.
    # ===========================================================================
    def _get_rule_implication(self, rdf_graph, rule_bnode):
        quote_graph = rdf_graph.triples((rule_bnode, Namespaces.REASON.gives, None)).next()[2]
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
    def parse_rest_services(self, rdf_graph, lemma_node):
        for _,_,rule_bnode  in rdf_graph.triples((lemma_node, Namespaces.REASON.rule, None)):
            implication_graph = self._get_rule_implication(rdf_graph, rule_bnode)
            return self._get_rest(implication_graph)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/partially_skolemized_plan.n3",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    rsp = RESTServicesParser( options.input )
    print rsp.calls