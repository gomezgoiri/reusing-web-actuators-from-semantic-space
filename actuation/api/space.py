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