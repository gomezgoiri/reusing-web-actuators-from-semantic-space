'''
Created on Sep 19, 2013

@author: tulvur
'''
from abc import ABCMeta
from actuation.api import Node


class RESTProvider(Node):
    
    __metaclass__ = ABCMeta # is it needed or is it inherited?
    
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



class Resource(object):
    
    def __init__(self):
        super(Resource, self).__init__()
        self.sub_resources = {} # key: subpath, value: resource_object

    def add_sub_resource(self, path, resource):
        self.sub_resources[path] = resource
    
    def _returnIfExists(self, resource_name, remaining_path):
        if resource_name in self.sub_resources: # usual case
            if remaining_path == "":
                return self.sub_resources[ resource_name ]
            else:
                return self.sub_resources[ resource_name ].get_sub_resource( remaining_path )
    
    def _join_strings_in_path(self, strings):
        if not strings: # empty
            return ""
        else:
            ret = ""
            for i in range( len(strings) ): # from 0 to N
                if ret == "": # first occurrence (or i==0)
                    ret = strings[i]
                else:
                    ret += "/" + strings[i]
            return ret
    
    def get_sub_resource(self, path):
        '''Path comes without the initial slash (e.g. bar/foo).'''
        # Maybe foo is not a sub_resource but foo/bar is
        parts = path.split("/")
        
        for i in range( len(parts) ): # from 0 to N
            resource_name = self._join_strings_in_path( parts[ : i+1 ] )
            remaining = self._join_strings_in_path( parts[ i+1 : len(parts) ] )            
            ret = self._returnIfExists(resource_name, remaining)
            if ret is not None:
                return ret
        return None
    
    def get_all_resources(self):
        ret = []
        for res in self.sub_resources.itervalues():
            ret.append( res )
            ret.extend( res.get_all_resources() )
        return ret
    
    def get_sub_resource_paths(self):
        return self.sub_resources.iterkeys()