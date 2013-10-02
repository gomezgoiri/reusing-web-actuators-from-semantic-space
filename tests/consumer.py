'''
Created on Sep 23, 2013

@author: tulvur
'''
import unittest
from random import shuffle
from mock import MagicMock
from actuation.api.rest import RESTProvider
from actuation.impl.rest.lamp.mock.consumer import LampConsumerRESTMock


class LampConsumerRESTMockTest(unittest.TestCase):


    def setUp(self):
        self.lc = LampConsumerRESTMock("", "", None)


    def tearDown(self):
        pass

    def _create_mock_resources(self):
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

    def _create_mock_provider(self):
        provider = FakeProvider()
        provider.get_all_resources = MagicMock()
        provider.get_all_resources.return_value = self._create_mock_resources()
        return provider
    
    def test_obtain_resource_descriptions(self):
        self.lc.discover( self._create_mock_provider(), "fakename" )
        self.lc._obtain_resource_descriptions()
        
        expected = ["desc%d"%i for i in range(1,4)]
        expected.extend( ["desc1%d"%i for i in range(4,6)] )
        expected.extend( ["desc2%d"%i for i in range(4,6)] )
        self.assertItemsEqual( expected, self.lc.descriptions )
    
    def test_get_node(self):
        nodes = []
        for _ in range(3):
            nodes.append( self._create_mock_provider() )
        
        self.lc.discover( nodes[0], "node1.deusto.es" )
        self.lc.discover( nodes[1], "node2.deustotech.eu" )
        self.lc.discover( nodes[2], "node.morelab.deusto.es" )
        
        self.assertEquals( self.lc.get_node( "http://node1.deusto.es/res1" ), (nodes[0], "/res1") )
        self.assertEquals( self.lc.get_node( "http://node2.deustotech.eu/res4/" ), (nodes[1], "/res4/") )
        self.assertEquals( self.lc.get_node( "http://node.morelab.deusto.es/lamp/light" ), (nodes[2], "/lamp/light") )
        self.assertIsNone( self.lc.get_node( "http://node.unexisting.com/resource/1" ) )


# I don't directly use MagicMock, because I need it to be a child of RESTProvider
class FakeProvider(RESTProvider):
    
    def start(self):
        pass
    
    def stop(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()