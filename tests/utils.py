'''
Created on Oct 4, 2013

@author: tulvur
'''
import re
import unittest
from actuation.utils import _construct_sparql_select, _parse_prefixes, _extract_uncommented_premise, _parse_variable_names


goal1 = """
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


class TestUtils(unittest.TestCase):

    # n3ql_to_sparql is indirectly tested through its subfunctions' tests:
    #    + test_construct_sparql_select_fail
    #    + test_construct_sparql_select_without_prefixes
    #    + test_n3ql_to_sparql

    def test_construct_sparql_select_fail(self):
        try:
            _construct_sparql_select({}, [], "?s ?p ?o .")
            self.fail()
        except:
            pass
    
    def test_construct_sparql_select_without_prefixes(self):
        q = _construct_sparql_select({}, ["s","p","o"], "?s ?p ?o .")
        ptt = re.compile( "^\s*select \s*[?]s, [?]p, [?]o\s*where\s*{\s*[?]s [?]p [?]o .\s*}", re.MULTILINE | re.DOTALL )
        self.assertTrue( ptt.search(q) )

    def test_parse_prefixes(self):
        expected = { "": "http://example.org/lamp/",
                     "sweet": "http://sweet.jpl.nasa.gov/",
                     "dul": "http://www.loa.istc.cnr.it/ontologies/DUL.owl#",
                     "ssn": "http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#",
                     "ucum": "http://purl.oclc.org/NET/muo/ucum/",
                     "actuators": "http://example.org/lamp/actuators/" }
        got = _parse_prefixes( goal1 )
        self.assertEquals( got, expected )
    
    def test_extract_uncommented_premise(self):
        lines = ["actuators:light ssn:madeObservation ?light .",
                 "?light ssn:observedProperty  sweet:Light ;",
                 "ssn:observationResult ?so .",
                 "?so ssn:hasValue ?ov .",
                 "?ov a ssn:ObservationValue ;",
                 "dul:isClassifiedBy  ucum:lux ;",
                 "dul:hasDataValue 19 ." ]
        got = _extract_uncommented_premise( goal1 )
        
        for l in got.split("\n"):
            st = l.strip()
            if st!="":
                self.assertTrue( l.strip() in lines, l + " was not expected" )
    
    def test_parse_variable_names(self):
        got = _parse_variable_names( "?v1 \n?v2\n blahblah? ?v3 ." )
        self.assertItemsEqual(got, ("v1", "v2", "v3"))



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()