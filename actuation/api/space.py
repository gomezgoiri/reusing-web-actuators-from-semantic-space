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
    def read_by_wildcard(self, template):
        pass
    
    @abstractmethod
    def read_by_sparql(self, query):
        pass
    
    @abstractmethod
    def take_by_wildcard(self, template):
        pass
    
    @abstractmethod
    def take_by_sparql(self, query):
        pass
    
    @abstractmethod
    def take_by_uri(self, uri):
        pass
    
    @abstractmethod
    def subscribe(self, template, callback):
        pass


class AbstractCallback(object):
    
    __metaclass__ = ABCMeta

    @abstractmethod
    def call(self):
        pass


class AbstractSubscriptionTemplate(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def matches(self, graph):
        pass


class AbstractSubscriptionObserver(object): # local observer
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def notify_subscription(self, template):
        pass