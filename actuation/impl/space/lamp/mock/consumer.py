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
from actuation.impl.space import CoordinationSpace
from actuation.impl.space import SPARQLSubscriptionTemplate


class LampConsumerSpaceMock(Node, AbstractCallback):
    
    def __init__(self, space, input_folder, output_folder, debug = False):
        self.space = space
        self.task_file_tpl = input_folder + "task.n3.tpl"
        self.task_file = output_folder + "task.n3"
        self.result_tpl = input_folder + "task_result.sparql.tpl"
        self.result_subs_file = output_folder + "task_result.sparql"
        self.__debug = debug
    
    def start(self):
        pass
    
    def stop(self):
        pass
    
    def __read_graph(self, filepath_or_stringio):
        g = Graph()
        g.parse( filepath_or_stringio, format="n3" )
        return g
    
    def _create_light_task_graph(self, value):
        with open( self.task_file_tpl, "r" ) as input_file:
            template = Template( input_file.read() )
            outc = template.render( value = value )
            ret = self.__read_graph( StringIO(outc) )
            if self.__debug:
                ret.serialize( self.task_file, format="n3" )
            return ret
    
    def write_task(self, light_value):
        self.space.write( self._create_light_task_graph( light_value ) ) # do nothing with the URI of the graph
    
    def __create_task_result_subscription(self, light_value):
        #pathname = mkstemp( suffix=".sparql", prefix="result_subs_", dir=self.output_folder)[1]
        with open( self.result_tpl, "r" ) as subscription_tpl_file:
            template = Template( subscription_tpl_file.read() )
            outc = template.render( value = light_value )
            if self.__debug:
                with open( self.result_subs_file, "w" ) as subscription_file:
                    subscription_file.write( outc )
            return SPARQLSubscriptionTemplate( outc )
    
    def subscribe_to_result(self, light_value):
        self.subscription_to_result = self.__create_task_result_subscription(light_value)
        self.space.subscribe( self.subscription_to_result, self, level=CoordinationSpace.SPACE_LEVEL )
    
    def _extract_light_value(self, task):
        # simple and error prone like hell parsing
        dul = Namespace("http://www.loa.istc.cnr.it/ontologies/DUL.owl#")
        literal = task.objects(None, dul.hasDataValue).next()
        return literal.value
    
    def call(self):
        # if you extract it, no one else will use it again...
        task = self.space.read_by_sparql( self.subscription_to_result.query )
        val = self._extract_light_value( task )
        #print val