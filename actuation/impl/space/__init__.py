'''
Created on Oct 2, 2013

@author: tulvur
'''

from rdflib.plugins.sparql import prepareQuery
from actuation.api.space import Space, AbstractSubscriptionTemplate
from otsopy.dataaccess.store import DataAccess
from actuation.utils.conversors import QueryLanguageConversor


class CoordinationSpace(Space):
    
    GRAPH_LEVEL = 0
    SPACE_LEVEL = 1 
    
    def __init__(self, space_name):
        self._da = DataAccess( defaultSpace = space_name )
        self._subscriptions = [] # tuple: (subscription template, callback, level)
        self._observers = []
    
    def write(self, triples):
        ret = self._da.write(triples)
        
        # TODO do it in another thread!
        activated = self._get_activated_subscriptions( triples )
        if activated:
            for ac in activated:
                ac.call()
        
        return ret
    
    def _get_activated_subscriptions(self, graph):
        ret = []
        for template, callback, level in self._subscriptions:
            if level == CoordinationSpace.GRAPH_LEVEL:
                if template.matches( graph ):
                    ret.append( callback )
            elif level == CoordinationSpace.SPACE_LEVEL:
                # over all the space!
                if template.matches( self._da.get_space(None).graphs ):
                    ret.append( callback )
            else:
                raise Exception( "Level %d does not exist" % level )
        return ret
    
    def read_by_wildcard(self, template):
        return self._da.read_wildcard( *template )
    
    def read_by_sparql(self, query):
        return self._da.read_sparql( query )
    
    def take_by_wildcard(self, template):
        return self._da.take_wildcard( *template )
    
    def take_by_sparql(self, query):
        return self._da.take_sparql( query )
    
    def take_by_uri(self, graph_uri):
        return self._da.take_uri( graph_uri )
    
    def query_by_sparql(self, query):
        return self._da.query_sparql( query )
    
    def subscribe(self, template, callback, level = 0 ):
        self._subscriptions.append( (template, callback, level) )
        # warn to the observers if any
        for observer in self._observers:
            if level == CoordinationSpace.SPACE_LEVEL: # not necessarily, but to filter in this scenario...
                observer.notify_subscription( template )
    
    def add_subscription_observer(self, observer):
        self._observers.append( observer )


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


# TODO deprecate
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


class SPARQLSubscriptionTemplate(AbstractSubscriptionTemplate):
    
    def __init__(self, query):
        """
        @param query: A SPARQL query
        """
        # E.g. 'select ?s where { ?person <http://xmlns.com/foaf/0.1/knows> ?s .}'
        self.query = prepareQuery( query )
    
    def matches(self, graph):
        if not graph.query( self.query ):
            return False
        return True

class N3QLSubscriptionTemplate(SPARQLSubscriptionTemplate):
    
    def __init__(self, n3ql_query):
        """
        @param templates: A N3QL query
        """
        # E.g. 'select ?s where { ?person <http://xmlns.com/foaf/0.1/knows> ?s .}'
        super(N3QLSubscriptionTemplate, self).__init__( QueryLanguageConversor.n3ql_to_sparql( n3ql_query) )