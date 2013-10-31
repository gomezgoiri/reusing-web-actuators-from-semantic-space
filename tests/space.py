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
from mock import MagicMock
from StringIO import StringIO
from rdflib import Graph, Namespace
from actuation.impl.space import CoordinationSpace, SimpleSubscriptionTemplate, SPARQLSubscriptionTemplate


class CoordinationSpaceTest(unittest.TestCase):

    def setUp(self):
        example_ns = Namespace("http://example.org/lamp/")
        ucum_ns = Namespace("http://purl.oclc.org/NET/muo/ucum/")
        dul_ns = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
        ssn_ns = Namespace("http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#")
        
        self.space = CoordinationSpace("foo")
        self.subscription_templates = []
        self.subscription_templates.append( SimpleSubscriptionTemplate( (example_ns.nonexistent, None, None) ) )
        self.subscription_templates.append( SimpleSubscriptionTemplate( (example_ns.obsv1, None, None) ) )
        self.subscription_templates.append( SimpleSubscriptionTemplate( (None, dul_ns.isClassifiedBy, None) ) )
        self.subscription_templates.append( SimpleSubscriptionTemplate( (None, None, ucum_ns.watt) ) )
        
        self.subscription_templates.append( SPARQLSubscriptionTemplate("""
           prefix ssn:  <%s>
           prefix dul:  <%s>
            
            select ?obsv where {
                ?obsv a ssn:ObservationValue .
                ?obsv dul:hasDataValue 19 .   
            }
        """ % ( ssn_ns, dul_ns)
        ) )
        
        self.callback_objects = []
        for s in self.subscription_templates:
            subscriber = MagicMock()
            # and maybe also: subscriber.call.return_value = whatever )
            self.callback_objects.append( subscriber )
            self.space.subscribe( s, subscriber )
            
        graph_n3 = """
@prefix : <http://example.org/lamp/>.
@prefix ssn: <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>.
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/>.
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix frap: <http://purl.org/frap/>.

:obsv1 a ssn:ObservationValue ;
      dul:isClassifiedBy ucum:lux ;
      dul:hasDataValue 19 .
"""
        self.graph1 = Graph()
        self.graph1.parse( StringIO(graph_n3), format="n3" )
        

        graph_n3 = """
@prefix : <http://example.org/lamp/>.
@prefix ssn: <http://www.w3.org/2005/Incubator/ssn/ssnx/ssn#>.
@prefix ucum: <http://purl.oclc.org/NET/muo/ucum/>.
@prefix dul: <http://www.loa.istc.cnr.it/ontologies/DUL.owl#>.
@prefix frap: <http://purl.org/frap/>.

:obsv2 a ssn:ObservationValue ;
      dul:isClassifiedBy ucum:watt ;
      dul:hasDataValue 4 .
"""
        self.graph2 = Graph()
        self.graph2.parse( StringIO(graph_n3), format="n3" )

    def tearDown(self):
        pass
    
    def assert_contains_callbacks(self, l, yes):
        no = range( len(self.callback_objects) )
        for y in yes:
            no.remove(y)
            self.assertTrue( self.callback_objects[y] in l )
        for n in no:
            self.assertFalse( self.callback_objects[n] in l )
            
    
    def test_get_activated_subscriptions(self):
        subs = self.space._get_activated_subscriptions( self.graph1 )
        self.assert_contains_callbacks( subs, (1, 2, 4,) )        
        subs = self.space._get_activated_subscriptions( self.graph2 )
        self.assert_contains_callbacks( subs, (2, 3,) )


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()