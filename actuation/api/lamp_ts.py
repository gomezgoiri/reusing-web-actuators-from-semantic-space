'''
Created on Sep 19, 2013

@author: tulvur
'''

from abc import ABCMeta, abstractmethod

class Space(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def write(self, graph):
        pass
    
    @abstractmethod
    def read(self, template):
        pass
    
    @abstractmethod
    def subscribe(self, template, callback):
        pass


class AbstractCallback(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def call(self):
        pass