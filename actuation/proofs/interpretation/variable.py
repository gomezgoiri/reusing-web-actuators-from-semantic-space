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

from rdflib import Namespace

var_ns = Namespace("http://localhost/var#")
# Why do I use a new namespace?
# So EYE cannot know that I'm talking about a variable which will be bounded with TSC knowledge.
# Otherwise, EYE will treat it differently, so with my queries I will get a blank node.
# Instead, I want the same URI to appear in the result so I can look for it.
fake_ns = Namespace("http://fake.is/var#") 

class Variable(object):
    """Class which represents ?var in a expression"""
    
    def __init__(self, name):
        self.name = name
    
    def urize(self): # could it be considered as a reification?
        return var_ns[self.name]
    
    def fake_urize(self):
        return fake_ns[self.name]
    
    @staticmethod
    def create(possible_var):
        """
        If 'binding_name' is "http://localhost/var#x0" or ?x0, simply takes x0.
        
        @param possible_var: can be either a 'string' or a 'rdflib.URIRef'  
        """
        prefs = (var_ns, fake_ns, "?")
        for pref in prefs:
            if possible_var.startswith(pref): # startswith() works with URIRefs and Namespaces
                # if possible_var is a URIRef, [:] converts it to string
                return Variable( possible_var[ len(pref):] )
        else: return None
    
    def n3(self):
        return self.__repr__()
    
    def __str__(self):
        return self.__repr__()
    
    def __repr__(self):
        return "?%s" % self.name
    
    def __eq__(self, other):
        if isinstance(other, Variable):
            return self.name == other.name
        return False # If "other" belongs to a different class of is "None"
    
    def __hash__(self):
        return hash( self.name )