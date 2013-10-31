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

class AbstractDiscovery(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def get_node(self, url_address):
        pass
    
    @abstractmethod
    def get_nodes(self):
        pass