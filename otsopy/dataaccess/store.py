# -*- coding: utf-8 -*-
'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
          Pablo Orduña <pablo.orduna@deusto.es>
'''

import threading
import random

from copy import deepcopy
from rdflib import ConjunctiveGraph, Graph

from otsopy.dataaccess.util import locked


class DataAccess(object):
    def __init__(self, defaultSpace="default"):
        self.stores = {}
        self._defaultSpace = defaultSpace
        if defaultSpace is not None:
            self.stores[defaultSpace] = Store() # join not implemented yet
    
    def get_space(self, space):
        if space == None:
            space = self._defaultSpace
        if not self.stores.has_key(space):
            raise Exception("Space '%s' does not exist." % space)
        return self.stores[space]
    
    def get_spaces(self):
        return self.stores.keys()
    
    def join_space(self, space):
        """Joins the *space* identified by an URI."""
        self.stores[space] = Store()
    
    def leave_space(self, space):
        """Leaves a *space* identified by an URI."""
        del self.stores[space]
    
    def get_graph_uris(self, space=None):
        store = self.get_space(space)
        return store.get_graph_uris()
            
    def write(self, triples, space=None):
        """Writes a set of triples into a space."""
        store = self.get_space(space)
        return store.write(triples)
        
    def read_uri(self, uri, space=None):
        """Reads the graph identified by an *uri* from the *space*.
        If such graph does not exist, it returns *None*."""
        store = self.get_space(space)
        return store.read_uri(uri)
    
    def read_wildcard(self, subject, predicate, obj, space=None):
        """Reads a graph with a triple which matches a *template* from the *space*.
        This operation is non deterministic and returns *None* when no graph is found."""
        store = self.get_space(space)
        return store.read_wildcard(subject, predicate, obj)
    
    def read_sparql(self, query, space=None):
        """Reads a graph with a triple which matches a *query* from the *space*.
        This operation is non deterministic and returns *None* when no graph is found."""
        store = self.get_space(space)
        return store.read_sparql(query)
    
    def take_uri(self, uri, space=None):
        """Reads and removes a graph from the space."""
        store = self.get_space(space)
        return store.take_uri(uri)
    
    def take_wildcard(self, subject, predicate, obj, space=None):
        """Reads and removes a graph from the space."""
        store = self.get_space(space)
        return store.take_wildcard(subject, predicate, obj)
    
    def take_sparql(self, query, space=None):
        """Reads and removes a graph from the space."""
        store = self.get_space(space)
        return store.take_sparql(query)
    
    def query_wildcard(self, subject, predicate, obj, space=None):
        """Returns all the triples in a *space* which match the *template*."""
        store = self.get_space(space)
        return store.query_wildcard(subject, predicate, obj)
    
    def query_sparql(self, query, space=None):
        """Returns all the triples in a *space* which match the *query*."""
        store = self.get_space(space)
        return store.query_sparql(query)


class Store(object):
    def __init__(self, store='default'):
        self.graphs = ConjunctiveGraph(store)
        self._lock = threading.RLock()

    @locked
    def _print(self):
        print "Graph %r" % self.graphs
    
    @locked
    def get_graph_uris(self):
        return [ n.identifier for n in self.graphs.contexts() ]
    
    def __write_graph(self, graph):
        self._lock.acquire()
        while True:
            #new_uri = URIRef('http://otsopack/%s' % random.randint(0, 1000))
            new_id = str( random.randint(0, 1000) )
            if new_id in filter(lambda n: n.identifier!=new_id, self.graphs.contexts()):
                continue
            
            gr = self.graphs.get_context(new_id) #Graph(self.graphs.store, new_uri)
            gr += graph
            return new_id
    
    @locked
    def write(self, triples):        
        if not isinstance(triples, Graph):
            raise Exception("'triples' must be a Graph.")

        new_uri = self.__write_graph(triples)
        self._lock.release()
        return new_uri

    @locked
    def read_uri(self, uri):
        ret = Graph(self.graphs.store, uri)
        return deepcopy(ret) if ret else None
    
    @locked
    def read_wildcard(self, subject, predicate, obj):
        gr = self._find_graph(subject, predicate, obj)
        return deepcopy(gr)
    
    @locked
    def read_sparql(self, query):
        gr = self._find_graph_sparql(query)
        return deepcopy(gr)
    
    @locked
    def take_uri(self, uri):
        ret = None
        try:
            #context = URIRef(uri)
            #ret = Graph(self.graphs.store, uri)
            to_delete = self.graphs.get_context(uri)
            ret = deepcopy(to_delete)
            self.graphs.remove_context(to_delete)
        except KeyError:
            return None
        return ret if len(ret)>0 else None

    @locked
    def take_wildcard(self, subject, predicate, obj):
        ret = None
        try:
            to_delete = self._find_graph(subject, predicate, obj)
            if to_delete is not None:
                ret = deepcopy(to_delete)
                self.graphs.remove_context(to_delete)
        except KeyError:
            return None
        return ret
    
    @locked
    def take_sparql(self, query):
        ret = None
        try:
            to_delete = self._find_graph_sparql(query)
            if to_delete is not None:
                ret = deepcopy(to_delete)
                self.graphs.remove_context(to_delete)
        except KeyError:
            return None
        return ret
    
    @locked
    def query_wildcard(self, subject, predicate, obj):
        ret = Graph()
        for t in self.graphs.triples((subject, predicate, obj)):
            ret.add(t)
        return ret if len(ret)>0 else None
    
    @locked
    def query_sparql(self, query):
        ret = Graph()
        for t in self.graphs.query( query ):
            ret.add(t)
        return ret if len(ret)>0 else None

    def _find_graph(self, subject, predicate, obj):
        for graph in self.graphs.contexts(): #(subject, predicate, obj)):
            for _ in graph.triples((subject, predicate, obj)):
                return graph # if it has at least a triple matching that triple, we return the graph
        return None
    
    def _find_graph_sparql(self, query):
        for graph in self.graphs.contexts():
            for _ in graph.query( query ):
                return graph # if the graph match the  a triple matching that triple, we return the graph
        return None