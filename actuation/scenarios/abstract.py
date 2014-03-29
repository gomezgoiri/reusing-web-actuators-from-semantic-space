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

import os
from time import time
from tempfile import mkdtemp, mkstemp
from jinja2 import Template
from StringIO import StringIO
from rdflib import Graph
from shutil import rmtree
from optparse import OptionParser
from abc import ABCMeta, abstractmethod
from actuation.utils.files import append_slash_if_absent


class AbstractSimulation(object):
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, output_folder):
        self.nodes = {}
        self.output_folder = mkdtemp( dir = output_folder ) + "/"
        self.execution_time = None
    
    # new possible phase
    # def initialize(self):  
    
    def run(self):
        '''
        Runs the scenario where the consumer tries to change the light in the environment.
        '''        
        start = time()
        
        self.configure()
        
        for node in self.nodes.itervalues():
            node.start()
        
        self.starting_time = time() - start # elapsed
        
        start = time()
        self.execute()
        self.execution_time = time() - start # elapsed
        
        for node in self.nodes.itervalues():
            node.stop()
        
        if self.check():
            print "The scenario behaved as expected (%d s)." % (self.execution_time)
        else:
            print "The scenario didn't run as expected (%d s)." % (self.execution_time)
    
    @abstractmethod
    def configure(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def check(self):
        pass
    
    def clean(self):
        rmtree( self.output_folder )
    
    def _create_benchmarking_content_for_a_provider(self, tpl_fp, provider_number):
        with open( tpl_fp, "r" ) as input_file:
            template = Template( input_file.read() )
            outc = template.render( heater_names = ["domain%d"%provider_number] )
            return outc
    
    def _create_benchmarking_content(self, tpl_fp, num_providers):
        if num_providers>0:
            with open( tpl_fp, "r" ) as input_file:
                template = Template( input_file.read() )
                outc = template.render( heater_names = ["domain%d"%i for i in range(num_providers)] )
                return outc
    
    def _create_benchmarking_file(self, outstring):
        if outstring is not None:
            testfd, ret_filepath = mkstemp( dir=self.output_folder, suffix=".n3" )
            #with open( ret_filepath, "w" ) as output_file: ## with this, testfd would still need to be closed!
            with os.fdopen(testfd,'w') as output_file: ## need to close file handles
                output_file.write( outstring ) # to check their validity afterwards
            return ret_filepath
    
    def _get_additional_knowledge_graph(self, tpl_fp, num_providers):
        if num_providers>0:
            outc = self._create_benchmarking_content(tpl_fp, num_providers)
            if self._debug:
                self._create_benchmarking_file(outc)
            ret = Graph()
            ret.parse( StringIO(outc), format="n3" )
            return ret


def main( simulation_subclass ):
    parser = OptionParser()
    parser.add_option("-n", "--numProvs", dest="providers", type="int", default=1,
                      help="Number of providers which exist in the scenario tested.")
    parser.add_option("-i", "--input", dest="input",
                      help="Base directory where all the files used in the simulation are stored.")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default="/opt/eye/bin/eye.sh",
                      help = "Path to the EYE reasoner. E.g., '/opt/eye/bin/eye.sh'.")
    parser.add_option("-c", "--clean", dest = "clean", default="True",
                      help = "Specifies whether the output directory should be clean after the execution.")
    parser.add_option("-d", "--debug", dest = "debug", default="True",
                      help = "Generate messages and files to check afterwards.")
    options, _ = parser.parse_args()
    
    sim = simulation_subclass( append_slash_if_absent( options.input ),
                            append_slash_if_absent( options.output ),
                            # optional, not all the simulations will have it!
                            options.euler, # we do not expect a path there anymore
                            options.providers,
                            options.debug )
                            #None if options.euler is None else append_slash_if_absent( options.euler ) )
    
    sim.run()
    
    if options.clean.lower() == "true":
        sim.clean()