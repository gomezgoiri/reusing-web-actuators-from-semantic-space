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

from StringIO import StringIO
from jinja2 import Template
from rdflib import Graph, Namespace

from actuation.api import Node
from actuation.api.space import AbstractCallback
from actuation.impl.space import SPARQLSubscriptionTemplate


class LampProviderSpaceMock(Node, AbstractCallback):
    
    def __init__(self, space, input_folder, output_folder, val = 0, debug = False):
        super(LampProviderSpaceMock, self).__init__()
        self.space = space
        self.subscription_to_task = self.__create_task_subscription(
                                            input_folder + "task_subscription.sparql" )
        
        self.init_gpaths = ( input_folder + "lamp_ret.n3",
                             input_folder + "light_ret.n3")
        
        self.result_file_tpl = input_folder + "measure_ret.n3.tpl"
        self.result_file = output_folder + "measure_ret.n3"
        
        self.light_guri = None
        self.init_light_val = val
        self.__debug = debug
    
    def __create_task_subscription(self, subscription_filename):
        #frap_ns = Namespace("http://purl.org/frap/")
        #return SimpleSubscriptionTemplate( (None, RDF.type, frap_ns.Preference) )
        with open( subscription_filename, "r" ) as subscription_file:
            return SPARQLSubscriptionTemplate( subscription_file.read() )
    
    def start(self):
        for g_path in self.init_gpaths:
            g = self.__read_graph( g_path )
            self.space.write( g )
        
        self._replace_light_graph( self.init_light_val )
        del self.init_light_val
        
        self._subscribe_task()
    
    def stop(self):
        pass
    
    def __read_graph(self, filepath_or_stringio):
        g = Graph()
        g.parse( filepath_or_stringio, format="n3" )
        return g
    
    def _subscribe_task(self):
        self.space.subscribe(self.subscription_to_task, self)
    
    def _create_light_graph(self, value):
        with open( self.result_file_tpl, "r" ) as input_file:
            template = Template( input_file.read() )
            outc = template.render( id="whatever", value = value )
            ret = self.__read_graph( StringIO(outc) )
            if self.__debug:
                ret.serialize( self.result_file, format="n3" )
            return ret
    
    #:obsv a ssn:ObservationValue, frap:Preference ;
    #  dul:isClassifiedBy  ucum:lux ;
    #  dul:hasDataValue {{value}} .
    def _extract_light_value(self, task):
        # simple and error prone like hell parsing
        dul = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
        literal = task.objects(None, dul.hasDataValue).next()
        return literal.value
    
    def _replace_light_graph(self, value):
        if self.light_guri is not None:
            # do nothing with the graph returned => discard
            self.space.take_by_uri( self.light_guri )
        g = self._create_light_graph( value )
        self.light_guri = self.space.write( g )
    
    def call(self):
        task = self.space.take_by_sparql( self.subscription_to_task.query )
        val = self._extract_light_value( task )
        # Take care, if you write something that activates the same subscription,
        # it will enter in an endless loop.
        # To check it, simply uncomment this: ;-)
        # print "weeeee"
        self._replace_light_graph( val )