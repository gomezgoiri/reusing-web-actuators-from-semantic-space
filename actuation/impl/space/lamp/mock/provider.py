'''
Created on Oct 2, 2013

@author: tulvur
'''

from actuation.api import Node


class LampProviderSpaceMock(Node):
    
    def __init__(self, space):
        self.space = space
    
    def subscribe_task(self):
        pass