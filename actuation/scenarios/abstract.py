'''
Created on Sep 19, 2013

@author: tulvur
'''

from abc import ABCMeta, abstractmethod
from actuation.api import Node


class AbstractSimulation(Node):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def configure(self):
        pass
    
    @abstractmethod
    def run(self):
        '''
        Runs the scenario where the consumer tries to change the light in the environment.
        '''
        pass
    
    @abstractmethod
    def check(self):
        pass