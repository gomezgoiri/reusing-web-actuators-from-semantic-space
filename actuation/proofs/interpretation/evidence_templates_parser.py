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
from rdflib import Graph, Namespace
from actuation.proofs.interpretation.variable import Variable


log_ns = Namespace("http://www.w3.org/2000/10/swap/log#")



class Template(object):
    def __init__(self, triple):
        self.subject = self._substitute_with_variable_if_possible( triple[0] )
        self.predicate = self._substitute_with_variable_if_possible( triple[1] )
        self.object = self._substitute_with_variable_if_possible( triple[2] )
    
    def _substitute_with_variable_if_possible(self, element):
        var = Variable.create( element )
        return var if var is not None else element
    
    def _substitute_with_None_if_variable(self, element):
        return None if isinstance(element, Variable) else element
    
    def get_template(self):
        return ( self._substitute_with_None_if_variable(self.subject),
                 self._substitute_with_None_if_variable(self.predicate),
                 self._substitute_with_None_if_variable(self.object) )
    
    def get_variables(self):
        ret = set()
        for el in ( self.subject, self.predicate, self.object ):
            if isinstance(el, Variable):
                ret.add( el )
        return ret
    
    def n3(self):
        return "%s %s %s . \n" % (self.subject.n3(), self.predicate.n3(), self.object.n3())
    
    def __repr__(self):
        return "t(%s, %s, %s)" % ( self.subject, self.predicate, self.object )


class EvidenceTemplatesParser(object):   
    
    def __init__(self, bindings_path):        
        self.templates_by_lemma = {}
        self._process_bindings( bindings_path )
    
    def _process_bindings(self, bindings_file_path):
        rdf_graph = Graph()
        rdf_graph.parse(bindings_file_path, format="n3")
        
        for lemma,_,template  in rdf_graph.triples((None, log_ns.includes, None)):
            lemma_id = str(lemma)
            
            for template in template.triples((None, None, None)):
                if lemma_id not in self.templates_by_lemma:
                    self.templates_by_lemma[ lemma_id ] = []
                # there should be just one
                self.templates_by_lemma[ lemma_id ].append( Template( template ) )

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--rest_input", dest="input", default="../../../files/evidences.txt",
                      help="File to process")
    (options, args) = parser.parse_args()
    
    etp = EvidenceTemplatesParser( options.input )
    print etp.templates_by_lemma