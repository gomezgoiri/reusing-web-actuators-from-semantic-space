'''
Created on Sep 19, 2013

@author: tulvur
'''
from abc import ABCMeta
from actuation.api import Node


class LightProviderREST(Node):
    
    __metaclass__ = ABCMeta
    
    def __init__(self, lamp_resource, light_resource):
        self._lamp_resource = lamp_resource
        self._light_resource = light_resource

class LightConsumerREST(object):
    
    __metaclass__ = ABCMeta

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        self._goal = value
        