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

import unittest
from StringIO import StringIO
from rdflib import Graph, Literal, Variable
from actuation.proofs import Namespaces, RESTCall, Binding
from actuation.proofs.parser import LemmasParser


class TestParser(unittest.TestCase):
    
    def __get_prefix_line(self, name, namespace):
        return "@prefix %s: <%s>.\n" % (name, namespace)        
    
    def __get_prefixes_snippet(self):
        ret = ""
        ret += self.__get_prefix_line("e", Namespaces.E)
        ret += self.__get_prefix_line("fake", Namespaces.FAKE)
        ret += self.__get_prefix_line("http", Namespaces.HTTP)
        ret += self.__get_prefix_line("log", Namespaces.LOG)
        ret += self.__get_prefix_line("n3", Namespaces.N3)
        ret += self.__get_prefix_line("r", Namespaces.REASON)
        ret += self.__get_prefix_line("var", Namespaces.VAR)
        return ret + "\n"
    
    def __get_rdf_graph(self, rdf_triple):
        content = self.__get_prefixes_snippet()
        content += rdf_triple
        rdf_graph = Graph()
        rdf_graph.parse(StringIO(content), format="n3")
        return rdf_graph
    
    def test_parse_lemma_evidences(self):
        rdf_graph = self.__get_rdf_graph("""
fake:lemma1 a r:Inference;
            r:evidence ( fake:lemma2 fake:lemma3 fake:lemma4 ) .
fake:lemma2 a r:Inference .
fake:lemma4 a r:Inference .
          """ )
        parser = LemmasParser(rdf_graph)
        
        precedences = parser._parse_lemma_evidences(Namespaces.FAKE.lemma1)
        self.assertTrue( Namespaces.FAKE.lemma2 in precedences )
        self.assertTrue( Namespaces.FAKE.lemma4 in precedences )
        self.assertFalse( Namespaces.FAKE.lemma3 in precedences )
    
    def test_parse_variable(self):
        rdf_graph = self.__get_rdf_graph('fake:whatever r:variable [ n3:uri "http://localhost/var#x0"] .')
        #'fake:whatever r:binding [ r:variable [ n3:uri "http://localhost/var#x0"] ] .'
        parser = LemmasParser(rdf_graph)
        var = parser._parse_variable(Namespaces.FAKE.whatever);
        self.assertEqual(var, Literal(Namespaces.VAR.x0))
        
    def test_parse_boundTo_number(self):
        rdf_graph = self.__get_rdf_graph('fake:whatever r:boundTo 30 .')
        parser = LemmasParser(rdf_graph)
        boundTo = parser._parse_boundTo(Namespaces.FAKE.whatever);
        self.assertEqual(boundTo, Literal(30))
        
    def test_parse_boundTo_uri(self):
        rdf_graph = self.__get_rdf_graph('fake:whatever r:boundTo [ n3:uri "%s"] .' % Namespaces.FAKE.deusto )
        parser = LemmasParser(rdf_graph)
        boundTo = parser._parse_boundTo(Namespaces.FAKE.whatever);
        self.assertEqual(boundTo, Literal(Namespaces.FAKE.deusto))
        
    def test_parse_bindings(self):
        b1 = Binding(Literal(Namespaces.VAR.x1), Literal(15))
        b2 = Binding(Literal(Namespaces.VAR.x0), Literal(4))
        b3 = Binding(Literal(Namespaces.VAR.x0), Literal(Namespaces.FAKE.ojocuidao))
        
        rdf_graph = self.__get_rdf_graph("""
            fake:whatever1 r:binding [ r:variable [ n3:uri "http://localhost/var#x1"]; r:boundTo 15 ] .
            fake:whatever2 r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; r:boundTo 4 ] .
            fake:whatever1 r:binding [ r:variable [ n3:uri "http://localhost/var#x0"]; r:boundTo [ n3:uri "%s" ]] .
        """ % Namespaces.FAKE.ojocuidao )
        parser = LemmasParser(rdf_graph)
        
        binds = parser._parse_bindings(Namespaces.FAKE.whatever1)
        self.assertTrue( b1 in binds )
        self.assertTrue( b3 in binds )
        
        binds = parser._parse_bindings(Namespaces.FAKE.whatever2)
        self.assertTrue( b2 in binds )
    
    def test_get_rule_implication(self):
        rdf_graph = self.__get_rdf_graph( """
            fake:whatever1 r:gives {
                fake:premise => fake:consequence .
            }.""" )
        parser = LemmasParser(rdf_graph)
        implication = parser._get_rule_implication(Namespaces.FAKE.whatever1)
        self.assertEquals(implication, Namespaces.FAKE.consequence)
    
    def test_parse_rest_services(self):
        rdf_graph = self.__get_rdf_graph("""
            fake:whatever1 r:rule [ r:gives {
                @forAll var:x0, var:x1.
                {
                    fake:premise
                } => {
                    var:x2 http:methodName "POST".
                    var:x2 http:requestURI <%s>.
                    var:x2 http:body var:x1.
                }
            } ].
        """ % Namespaces.FAKE.ojocuidao )
        parser = LemmasParser(rdf_graph)
        rest = parser._parse_rest_services(Namespaces.FAKE.whatever1)
        expected = RESTCall( Literal("POST"), Namespaces.FAKE.ojocuidao, Variable("x1") )
        self.assertEquals( rest, expected )


if __name__ == "__main__":
    unittest.main()