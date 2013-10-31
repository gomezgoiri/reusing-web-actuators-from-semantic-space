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
from actuation.api.rest import RESTProvider
from actuation.impl.rest.lamp.resources import Resource

# Tests RESTProvider and Resource
class RESTProviderTest(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_join_strings_in_path(self):
        rsc = Resource()
        self.assertEquals( rsc._join_strings_in_path(None), "" )
        self.assertEquals( rsc._join_strings_in_path(["boo"]), "boo" )
        self.assertEquals( rsc._join_strings_in_path(["boo","bah"]), "boo/bah" )
        self.assertEquals( rsc._join_strings_in_path(["carabi","ru","ri"]), "carabi/ru/ri" )

    def _create_nested_resources(self):
        # id attribute does not exist in Resource, but I use it for testing
        rsc = Resource()
        rsc.id = "res1"
        
        rsc2 = Resource()
        rsc2.id = "res2"
        rsc.sub_resources["foo"] = rsc2
        
        rsc3 = Resource()
        rsc3.id = "res3"
        rsc2.sub_resources["bar"] = rsc3
        
        rsc4 = Resource()
        rsc4.id = "res4"
        rsc.sub_resources["foo/bash"] = rsc4
        
        return rsc
    
    def _create_provider(self):        
        provider = ConcreteProvider()
        provider.resources['mock'] = self._create_nested_resources()
        return provider
    
    def test_get_sub_resource(self):
        rsc = self._create_nested_resources()
        
        # the path must not contain an initial slash,RESTProviderRESTProvider but it also works
        self.assertEquals( "res2", rsc.get_sub_resource("/foo").id )
        
        self.assertEquals( "res2", rsc.get_sub_resource("foo").id ) # obtains it directly from rsc
        self.assertEquals( "res3", rsc.get_sub_resource("foo/bar").id ) # obtains it from rsc2
        self.assertEquals( "res4", rsc.get_sub_resource("foo/bash").id ) # obtains it directly from rsc
        
        self.assertIsNone( rsc.get_sub_resource("foo/bar/moo") )
        self.assertIsNone( rsc.get_sub_resource("push") )
        
    
    def test_get_all_resources(self):
        # Testing RESTProvider's get_all_resources method
        prov = self._create_provider()
        rscs = prov.get_all_resources()
        ids = [r.id for r in rscs]
        self.assertItemsEqual( ['res%d'%(i) for i in range(1,5)], ids )
        
        # Testing Resource's get_all_resources method
        rsc = self._create_nested_resources()
        rscs = rsc.get_all_resources()
        ids = [r.id for r in rscs]
        self.assertItemsEqual( ['res%d'%(i) for i in range(2,5)], ids )
    
    def test_get_resource(self):
        prov = self._create_provider()
        
        self.assertIsNone( prov.get_resource("/") )
        self.assertIsNone( prov.get_resource("/yipi/kai/yei") )
        
        self.assertEquals( "res1", prov.get_resource("/mock").id ) # get root resource
        # if the following works, the rest cases from test_get_sub_resource will also work
        self.assertEquals( "res3", prov.get_resource("/mock/foo/bar").id )


class ConcreteProvider(RESTProvider):
    def start(self):
        pass
    
    def stop(self):
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()