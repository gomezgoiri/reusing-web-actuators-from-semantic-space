'''
Created on Sep 19, 2013

@author: tulvur
'''
from abc import ABCMeta
from actuation.api import Node


class RESTProvider(Node):
    
    def __init__(self):
        super(RESTProvider,self).__init__()
        # Just the "root resources", the rest should be discovered iteratively
        self.resources = {} # Key: url (partial or not); Value: resource
    
    # the path expressed as /foo/bar
    def get_resource(self, path):
        if path.startswith("/"):
            part = path[1:].partition("/")
            
            if part[0] in self.resources:
                if part[2] == "":
                    return self.resources[ part[0] ]
                else:
                    return self.resources[ part[0] ].get_sub_resource( part[2] )
        
        return None
    
    def get_all_resources(self):
        ret = []
        for res in self.resources.itervalues():
            ret.append( res )
            ret.extend( res.get_all_resources() )        
        return ret


class LampConsumerREST(Node):
    
    __metaclass__ = ABCMeta

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, value):
        self._goal = value
        