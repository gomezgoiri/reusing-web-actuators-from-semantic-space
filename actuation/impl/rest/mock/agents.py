# -*- coding: utf-8 -*-
'''
 Copyright (C) 2013 onwards University of Deusto
  
 All rights reserved.
 
 This software is licensed as described in the file COPYING, which
 you should have received as part of this distribution.
 
 This software consists of contributions made by many individuals, 
 listed below:
 
 @author: Aitor Gómez Goiri <aitor.gomez@deusto.es>
'''

from actuation.api.rest import RESTProvider

class Crawler(object):
    
    def __init__(self, discovery):
        self.discovery = discovery
        self._descriptions = set()
        self._base_knowledge = set()
    
    # or directly update in the constructor
    def update(self):
        self._obtain_resource_descriptions()
        self._obtain_base_knowledge()
    
    def _obtain_resource_descriptions(self):
        for node in self.discovery.get_nodes():
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'options'): # maybe it does not implement it
                        opts = resource.options()
                        if hasattr(opts, '__iter__'):
                            self._descriptions.update( opts ) # == extend in lists
                        else:
                            self._descriptions.add( opts ) # == append in lists
     
    def _obtain_base_knowledge(self):
        '''Crawling to obtain base knowledge (done by an spider, autonomous agent)'''
        for node in self.discovery.get_nodes():
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'get'): # maybe it does not implement it
                        opts = resource.get()
                        self._base_knowledge.add( opts ) # == append in lists
    
    @property
    def descriptions(self):
        return self._descriptions
    
    @property
    def base_knowledge(self):
        return self._base_knowledge


class PlanAchiever(object):
    
    def __init__(self, lgraph, discovery):
        self.lgraph = lgraph
        self.discovery = discovery
    
    def __make_call(self, lemma):
        # TODO the output of a call should be parsed: it may be the input of another one
        nret = self.discovery.get_node( lemma.rest.request_uri )
        if nret:
            node, remaining_path = nret
            rsc = node.get_resource( remaining_path )
            
            if rsc is None:
                print "Resource '%s' not found in node." % (remaining_path)
            else:
                met = str(lemma.rest.method)
                if met == "POST":
                    body = lemma.get_binding( lemma.rest.var_body )
                    return rsc.post( body )
                elif met == "GET":
                    return rsc.get()
                else:
                    raise Exception( "TODO, HTTP verb: %s" % (lemma.rest.method) )
        else:
            print "Node not found"
        
    
    def achieve(self):
        for n in self.lgraph.get_shortest_path():
            #print n
            if n.is_rest_call():
                # deliberated ignore of the return
                # in this project we just check a simple path composed by a unique rest call 
                self.__make_call( n )