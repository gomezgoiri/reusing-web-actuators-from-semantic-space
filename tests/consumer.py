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
from random import shuffle
from mock import MagicMock
from actuation.api.rest import RESTProvider
from actuation.impl.rest.mock.discovery import MockDiscovery
from actuation.impl.rest.mock.agents import Crawler


# Through these 2 classes, we indirectly test LampConsumerRESTMock

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        self.discovery = MockDiscovery()        
        self.discovery.add_discovered( ProvidersFactory.create_mock_providers(), "fakename" )
        self.crawler= Crawler( self.discovery )
    
    def test_obtain_resource_descriptions(self):
        self.crawler._obtain_resource_descriptions()
        
        expected = ["desc%d"%i for i in range(1,4)]
        expected.extend( ["desc1%d"%i for i in range(4,6)] )
        expected.extend( ["desc2%d"%i for i in range(4,6)] )
        self.assertItemsEqual( expected, self.crawler.descriptions )


class DiscoveryMockTest(unittest.TestCase):
    
    def setUp(self):
        self.discovery = MockDiscovery()
    
    def _create_node(self, name):
        ret = ProvidersFactory.create_mock_providers()
        self.discovery.add_discovered( ret, name )
        return ret
    
    def test_get_node(self):
        nodes = []
        for name in ("node1.deusto.es" , "node2.deustotech.eu" , "node.morelab.deusto.es"):
            nodes.append( self._create_node( name ) )
        
        self.assertEquals( self.discovery.get_node( "http://node1.deusto.es/res1" ), (nodes[0], "/res1") )
        self.assertEquals( self.discovery.get_node( "http://node2.deustotech.eu/res4/" ), (nodes[1], "/res4/") )
        self.assertEquals( self.discovery.get_node( "http://node.morelab.deusto.es/lamp/light" ), (nodes[2], "/lamp/light") )
        self.assertIsNone( self.discovery.get_node( "http://node.unexisting.com/resource/1" ) )



# I don't directly use MagicMock, because I need it to be a child of RESTProvider
class FakeProvider(RESTProvider):
    
    def start(self):
        pass
    
    def stop(self):
        pass


class ProvidersFactory(object):
    
    @staticmethod
    def _create_mock_resources():
        resources = []
        
        for i in range(1,4): # one rule returned
            mock = MagicMock()
            mock.options.return_value = "desc%d" % i 
            resources.append( mock )
        
        for i in range(4,6): # more than a rule returned by HTTP OPTIONS
            mock = MagicMock()
            mock.options.return_value = ["desc1%d" % i, "desc2%d" % i] 
            resources.append( mock )
            
        for i in range(6,9): # without HTTP OPTIONS
            no_http_options_object = object()
            resources.append( no_http_options_object )
        
        shuffle(resources)
        return resources
    
    @staticmethod
    def create_mock_providers():
        provider = FakeProvider()
        provider.get_all_resources = MagicMock()
        provider.get_all_resources.return_value = ProvidersFactory._create_mock_resources()
        return provider



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()