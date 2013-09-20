'''
Created on Sep 19, 2013

@author: tulvur
'''
from abc import ABCMeta
from actuation.api import Node


class RESTProvider(Node):
    
    def __init__(self):
        super(RESTProvider,self).__init__()
        self.resources = {} # Key: url (partial or not); Value: resource

class LightProviderREST(RESTProvider):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, lamp_resource, light_resource):
        super(LightProviderREST,self).__init__()
        
        # TODO it should correspond with the description!
        self.resources['/lamp'] = lamp_resource
        self.resources['/lamp/light'] = light_resource


class LightConsumerREST(Node):
    
    __metaclass__ = ABCMeta

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        self._goal = value
        