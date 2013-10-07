'''
Created on Oct 2, 2013

@author: tulvur
'''

from StringIO import StringIO
from jinja2 import Template
from rdflib import Graph

from actuation.api import Node


class LampConsumerSpaceMock(Node):
    
    def __init__(self, space, input_folder, output_folder, debug = False):
        self.space = space
        self.task_file_tpl = input_folder + "task.n3.tpl"
        self.task_file = output_folder + "task.n3"
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
    
    def _get_light_to_value_task_graph(self, value):
        if self.light_guri is not None:
            # do nothing with the graph returned => discard
            self.space.take_by_uri( self.light_guri )
        g = self._create_light_graph( value )
        self.light_guri = self.space.write( g )
    
    def write_task(self):
        self.space.write( self._create_light_task_graph(30) )