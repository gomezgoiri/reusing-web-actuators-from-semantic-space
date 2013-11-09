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
from rdflib import Graph, RDF
from actuation.proofs import Lemmas, Namespaces
from actuation.proofs.parsers.bindings import BindingsParser
from actuation.proofs.parsers.rest import RESTServicesParser
from actuation.proofs.parsers.evidence_templates import EvidenceTemplatesParser
    
# This can be interesting: https://github.com/RDFLib/rdflib/blob/master/docs/persisting_n3_terms.rst

class LemmasParser(object):
    """
    This class parses what a lemma contains or may contain:
      * evidence template patterns
      * bindings
      * rest services
    """
    
    @staticmethod
    def _parse_lemma( rdf_graph, lemmas ):
        for lemma,_,_  in rdf_graph.triples((None, RDF.type, Namespaces.REASON.Inference)):            
            bp = BindingsParser()
            bindings = bp.parse_bindings(rdf_graph, lemma)
            lemmas.add_bindings( lemma, bindings )
            
            rp = RESTServicesParser()
            rest = rp.parse_rest_services(rdf_graph, lemma)
            if rest is not None:
                lemmas.add_rest_call( lemma, rest )
    
    
    @staticmethod
    def parse_file( plan_file_path, rest_file_path, bindings_path, evidences_path):
        lemmas = Lemmas()
        
        rdf_graph = Graph()
        rdf_graph.parse(plan_file_path, format="n3")
        LemmasParser._parse_lemma(rdf_graph, lemmas)
            
        etp = EvidenceTemplatesParser( evidences_path )
        for lemma, templates in etp.templates_by_lemma.iteritems():
            lemmas.add_evidence_templates( lemma, templates )
        
        return lemmas


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-r", "--rest_input", dest="rest", default="../../../files/services.txt",
                      help="REST services file.")
    parser.add_option("-b", "--bindings", dest="bindings", default="../../../files/bindings.txt",
                      help="Bindings file.")
    parser.add_option("-e", "--evidences", dest="evidences", default="../../../files/evidences.txt",
                      help="Evidences file.")
    (options, args) = parser.parse_args()
    
    print LemmasParser.parse_file( options.rest, options.bindings, options.evidences )