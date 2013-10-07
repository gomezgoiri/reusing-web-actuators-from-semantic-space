'''
Created on Oct 7, 2013

@author: tulvur
'''

from abc import ABCMeta, abstractmethod

class AbstractDiscovery(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_node(self, url_address):
        pass
    
    @abstractmethod
    def get_nodes(self):
        pass