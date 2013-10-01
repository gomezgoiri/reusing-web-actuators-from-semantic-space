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
from actuation.proofs import Lemmas
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
    def parse_file( rest_file_path, bindings_path, evidences_path):
        lemmas = Lemmas()
        
        bp = BindingsParser( bindings_path ) 
        for lemma, bindings in bp.bindings_by_lemma.iteritems():
            lemmas.add_bindings( lemma, bindings )
            
        rp = RESTServicesParser( rest_file_path )
        for lemma, rest in rp.calls.iteritems():
            lemmas.add_rest_call( lemma, rest )
            
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