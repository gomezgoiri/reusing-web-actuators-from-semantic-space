'''
Created on Oct 2, 2013

@author: tulvur
'''

from actuation.api import Node


class LampConsumerSpaceMock(Node):
    
    def __init__(self, space):
        self.space = space
    
    def write_task(self):
        pass