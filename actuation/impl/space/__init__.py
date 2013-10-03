'''
Created on Oct 2, 2013

@author: tulvur
'''

from actuation.api.space import Space, AbstractSubscriptionTemplate
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
    
    def _get_activated_subscriptions(self, graph):
        ret = []
        for template, callback in self._subscriptions:
            if template.matches( graph ):
                ret.append( callback )
        return ret
    
    def read(self, template):
        return self._da.read_wildcard( *template )
    
    def take(self, template):
        return self._da.take_wildcard( *template )
    
    def take_by_uri(self, graph_uri):
        return self._da.take_uri( graph_uri )
    
    def subscribe(self, template, callback):
        self._subscriptions.append( (template, callback) )


class SimpleSubscriptionTemplate(AbstractSubscriptionTemplate):
    
    def __init__(self, template):
        self.template = template
    
    def __has_next(self, generator):
        try:
            generator.next()
            return True
        except:
            # no triple in the generator
            return False
    
    def matches(self, graph):
        t = graph.triples( self.template )
        return self.__has_next(t)

    
class AggregationSubscriptionTemplate(AbstractSubscriptionTemplate):
    
    def __init__(self, templates):
        """
        @param templates: A list of SimpleSubscriptionTemplate objects
        """
        self.templates = templates
    
    def matches(self, graph):
        for t in self.templates:
            if not t.matches( graph ):
                return False
        return True