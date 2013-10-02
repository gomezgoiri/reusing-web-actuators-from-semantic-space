'''
Created on Oct 2, 2013

@author: tulvur
'''

from actuation.api.lamp_ts import Space
from actuation.impl.otsopy.dataaccess.store import DataAccess



class CoordinationSpace(Space):
    
    def __init__(self, space_name):
        self._da = DataAccess( defaultSpace = space_name )
        self._subscriptions = [] # tuple: (subscription template, callback)
    
    def write(self, triples):
        self._da.write(triples)
        # does not return the uri, unneeded in this case
        
        activated = self._get_activated_subscriptions( triples )
        if activated:
            for ac in activated:
                ac.call()
    
    def __has_next(self, generator):
        try:
            generator.next()
            return True
        except:
            # no triple in the generator
            return False
    
    def _get_activated_subscriptions(self, graph):
        ret = []
        for template, callback in self._subscriptions:
            t = graph.triples( template )
            if self.__has_next(t):
                ret.append( callback )
        return ret
    
    def read(self, template):
        return self._da.read_wildcard( *template )
    
    def subscribe(self, template, callback):
        self._subscriptions.append( (template, callback) )