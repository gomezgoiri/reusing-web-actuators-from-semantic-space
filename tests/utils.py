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

import re
import unittest
from rdflib.term import Variable
from actuation.utils.conversors import QueryLanguageConversor, N3QLParser


goal_n3ql = """
@prefix sweet:  <http://sweet.jpl.nasa.gov/> .
@prefix dul:  <http://www.loa.istc.cnr.it/ontologies/DUL.owl#> .
@prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#> .
@prefix ucum:  <http://purl.oclc.org/NET/muo/ucum/> .
@prefix actuators:  <http://example.org/lamp/actuators/> .
@prefix : <http://example.org/lamp/>.

{ # Analogy: SPARQL WHERE

  # More things could be specified here: location, whatever...
  
  actuators:light ssn:madeObservation ?light .
  
  ?light ssn:observedProperty  sweet:Light ;
         ssn:observationResult ?so .
  
  ?so ssn:hasValue ?ov .
  
  ?ov a ssn:ObservationValue ;
      dul:isClassifiedBy  ucum:lux ;
      dul:hasDataValue 19 .
  
  #?val op:greaterThan 19 .

}
=>
{ # Analogy: SPARQL CONSTRUCT

  ?ov  dul:hasDataValue  ?val .

}.
"""


sparql_query = """
prefix : <http://example.org/lamp/>
prefix sweet:  <http://sweet.jpl.nasa.gov/>
prefix ssn:  <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>
prefix actuators:  <http://example.org/lamp/actuators/>

select ?val where {
  actuators:light ssn:madeObservation ?light .
  # comment
  ?light ssn:observedProperty  sweet:Light ;
         ssn:observationResult ?so .
}
"""


class TestQueryLanguageConversor(unittest.TestCase):

    def setUp(self):
        self.qlc = QueryLanguageConversor()

    # QueryLanguageConversor is indirectly tested through its subfunctions' tests:
    #    + test_to_sparql_select_fail
    #    + test_to_sparql_select_without_prefixes
    #    + test_to_n3ql_goal
    #    + test_parse_sparql
    # ...and TestN3QLParser.

    def test_to_sparql_select_fail(self):
        try:
            self.qlc._variabs = []
            self.qlc._to_sparql_select()
            self.fail()
        except:
            pass        
    
    def test_to_sparql_select_without_prefixes(self):
        self.qlc._prefixes = {}
        self.qlc._variabs = ["s","p","o"]
        self.qlc._premise = "?s ?p ?o ."
        q = self.qlc._to_sparql_select()
        ptt = re.compile( "^\s*select \s*[?]s, [?]p, [?]o\s*where\s*{\s*[?]s [?]p [?]o .\s*}", re.MULTILINE | re.DOTALL )
        self.assertTrue( ptt.search(q) )
    
    def test_to_n3ql_goal(self):
        self.qlc._prefixes = {}
        self.qlc._variabs = ["s","p","o"]
        self.qlc._premise = "?s ?p ?o ."
        q = self.qlc._to_n3ql_goal()
        ptt = re.compile( "^\s*{\s*[?]s [?]p [?]o .\s*}\s*=>\s*{\s*[?]s [?]p [?]o .\s*}\s*.", re.MULTILINE | re.DOTALL )
        self.assertTrue( ptt.search(q) )
    
    def test_parse_sparql(self):
        # It is not necessary to test all cases, I assume that RDFLib is already tested.
        # Anyway, I'll check a basic case to test that I'm using RDFLib properly.
        self.qlc.parse( sparql_query, formAt="sparql" )
        self.assertItemsEqual( self.qlc._variabs, ( Variable("val"), Variable("light"), Variable("so") ) )
        # Like this, because I don't know the order of the lines in the serialization
        self.assertTrue( " <http://example.org/lamp/actuators/light> <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#madeObservation> ?light .\n" in self.qlc._premise )
        self.assertTrue( " ?light <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#observedProperty> <http://sweet.jpl.nasa.gov/Light> .\n" in self.qlc._premise )
        self.assertTrue( " ?light <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#observationResult> ?so .\n" in self.qlc._premise )


class TestN3QLParser(unittest.TestCase):
    
    def test_parse_prefixes(self):
        expected = { "": "http://example.org/lamp/",
                     "sweet": "http://sweet.jpl.nasa.gov/",
                     "dul": "http://www.loa.istc.cnr.it/ontologies/DUL.owl#",
                     "ssn": "http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#",
                     "ucum": "http://purl.oclc.org/NET/muo/ucum/",
                     "actuators": "http://example.org/lamp/actuators/" }
        got = N3QLParser._parse_prefixes( goal_n3ql )
        self.assertEquals( got, expected )
    
    def test_extract_uncommented_premise(self):
        lines = ["actuators:light ssn:madeObservation ?light .",
                 "?light ssn:observedProperty  sweet:Light ;",
                 "ssn:observationResult ?so .",
                 "?so ssn:hasValue ?ov .",
                 "?ov a ssn:ObservationValue ;",
                 "dul:isClassifiedBy  ucum:lux ;",
                 "dul:hasDataValue 19 ." ]
        got = N3QLParser._extract_uncommented_premise( goal_n3ql )
        
        for l in got.split("\n"):
            st = l.strip()
            if st!="":
                self.assertTrue( l.strip() in lines, l + " was not expected" )
    
    def test_parse_variable_names(self):
        got = N3QLParser._parse_variable_names( "?v1 \n?v2\n blahblah? ?v3 ." )
        self.assertItemsEqual(got, (Variable("v1"), Variable("v2"), Variable("v3")))


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()