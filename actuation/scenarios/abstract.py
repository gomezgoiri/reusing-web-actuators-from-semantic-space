'''
Created on Sep 19, 2013

@author: tulvur
'''

from abc import ABCMeta, abstractmethod


class AbstractSimulation(object):
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self):
        self.nodes = {}
    
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
            
        self.check()
    
    @abstractmethod
    def configure(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def check(self):
        pass