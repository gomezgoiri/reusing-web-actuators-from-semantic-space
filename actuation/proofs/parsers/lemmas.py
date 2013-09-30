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
from actuation.proofs import Lemma
from actuation.proofs.parsers.bindings import BindingsParser
from actuation.proofs.parsers.rest import RESTServicesParser
from actuation.proofs.parsers.evidence_templates import EvidenceTemplatesParser
    

class LemmasParser(object):
    """
    This class parses what a lemma contains or may contain:
      * evidence template patterns
      * bindings
      * rest services
    """
    
    def __init__(self, rest_file_path, bindings_path, evidences_path):
        self.lemmas = {}
        
        bp = BindingsParser( bindings_path ) 
        for lemma, bindings in bp.bindings_by_lemma.iteritems():
            self._init_lemma_if_needed(lemma)
            self.lemmas[lemma].bindings = bindings
        
        rp = RESTServicesParser( rest_file_path )
        for lemma, rest in rp.calls.iteritems():
            self._init_lemma_if_needed(lemma)
            self.lemmas[lemma].rest = rest
            
        etp = EvidenceTemplatesParser( evidences_path )
        for lemma, templates in etp.templates_by_lemma.iteritems():
            self._init_lemma_if_needed(lemma)
            self.lemmas[lemma].evidence_templates = templates
    
    def _init_lemma_if_needed(self, lemma):
        if lemma not in self.lemmas:
            self.lemmas[lemma] = Lemma()


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/services.txt",
                      help="REST services file.")
    parser.add_option("-b", "--bindings", dest="bindings", default="../../../files/bindings.txt",
                      help="Bindings file.")
    parser.add_option("-e", "--evidences", dest="evidences", default="../../../files/evidences.txt",
                      help="Evidences file.")
    (options, args) = parser.parse_args()
    
    lp = LemmasParser( options.input, options.bindings )
    print lp.lemmas