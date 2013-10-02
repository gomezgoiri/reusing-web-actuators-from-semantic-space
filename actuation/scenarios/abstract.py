'''
Created on Sep 19, 2013

@author: tulvur
'''

from abc import ABCMeta, abstractmethod
from tempfile import mkdtemp
from shutil import rmtree


class AbstractSimulation(object):
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, output_folder):
        self.nodes = {}
        self.output_folder = mkdtemp( dir = output_folder ) + "/"
    
    # new possible phase
    # def initialize(self):  
    
    def run(self):
        '''
        Runs the scenario where the consumer tries to change the light in the environment.
        '''
        self.configure()
        
        for node in self.nodes.itervalues():
            node.start()
        
        self.execute()
        
        for node in self.nodes.itervalues():
            node.stop()
        
        if self.check():
            print "The scenario behaved as expected."
        else:
            print "The scenario didn't run as expected."
    
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