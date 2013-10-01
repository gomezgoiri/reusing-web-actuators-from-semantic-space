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

from rdflib import URIRef, Namespace


'''
Domain classes used by the reasoner:
    + Namespaces provides the additional namespaces used both by Euler and this project.
    + Lemma, is composed by the rest of classes and together with other Lemmas forms a plan towards a goal.
    + Template which backs a lemma.
    + Binding between a variable and a value.
'''


class Namespaces(object):
    """
    Namespaces used both by Euler and this project.
    """
    
    HTTP = Namespace("http://www.w3.org/2011/http#")
    LOG = Namespace("http://www.w3.org/2000/10/swap/log#")
    REASON = Namespace("http://www.w3.org/2000/10/swap/reason#")
    VAR = Namespace("http://localhost/var#")
    # Why did I use a new namespace? // In this project is deprecated
    # So EYE cannot know that I'm talking about a variable which will be bounded with TSC knowledge.
    # Otherwise, EYE will treat it differently, so with my queries I will get a blank node.
    # Instead, I want the same URI to appear in the result so I can look for it.
    FAKE = Namespace("http://fake.is/var#")


class Lemmas(object):
    """
    This class is a collection of Lemma objects with some utility methods.
    
    Represents the result file of a Euler reasoning in memory.
    """
    
    def __init__(self):
        self._lemmas = {}
    
    def _get_and_create_if_not_exists(self, lemma_name):
        s_lname = str( lemma_name )
        if s_lname not in self._lemmas:
            self._lemmas[s_lname] = Lemma()
        return self._lemmas[s_lname]
            
    def add_bindings(self, lemma, bindings):
        self._get_and_create_if_not_exists( lemma ).bindings = bindings
    
    def add_rest_call(self, lemma, rest_call):
        self._get_and_create_if_not_exists( lemma ).rest = rest_call
    
    def add_evidence_templates(self, lemma, templates):
        self._get_and_create_if_not_exists( lemma ).evidence_templates = templates
    
    def get_lemma(self, lemma_name):
        s_lname = str( lemma_name )
        if s_lname in self._lemmas:
            return self._lemmas[s_lname]
        return None
    
    def __repr__(self):
        s = "( "
        for l in self._lemmas.iterkeys():
            if s is "( ":
                s += l
            else:
                s += ", " + l
        s += " )" 
        return s


class Lemma(object):
    """
    A lemma has some evidence templates (premises), a rest call (consequence) and some values to make that call (bindings). 
    """
    
    def __init__(self):
        self.rest = None
        self._bindings = set()
        self.evidence_templates = []
    
    def get_binding(self, var):
        for binding in self.bindings:
            if binding.variable == var:
                return binding.bound
        else: return None
    
    @property
    def bindings(self):
        return self._bindings
    
    @bindings.setter
    def bindings(self, bindings): # to ensure that bindings is a list and therefore can be compared with other list
        if isinstance(bindings, (list, tuple)):
            self._bindings = set(bindings)
        elif isinstance(bindings, set):
            self._bindings = bindings
        else:
            raise Exception("It should be a list, tuple or set!")
    
    def equivalent_rest_calls(self, other_lemma):
        ret = self.rest == other_lemma.rest and self.bindings == other_lemma.bindings # same bindings
        if ret:
            # TODO what if it is not a variable?
            if self.rest is not None: # therefore other_lemma.rest cannot be None either
                ret = self.get_binding( self.rest.var_body ) == other_lemma.get_binding( other_lemma.rest.var_body )
            
        return ret
    
    def is_rest_call(self):
        return self.rest is not None
    
    def __repr__(self):
        return "l(rest: %s, bindings: %s, evidences: %s)" % (self.rest, self.bindings, self.evidence_templates)



class Template(object):
    """
    It is composed by an subject, a predicate and an object.
    
    Each of these elements can have an actual value or be a variable.
    """
    
    def __init__(self, triple):
        self.subject = self._substitute_with_variable_if_possible( triple[0] )
        self.predicate = self._substitute_with_variable_if_possible( triple[1] )
        self.object = self._substitute_with_variable_if_possible( triple[2] )
    
    def _substitute_with_variable_if_possible(self, element):
        var = Variable.create( element )
        return var if var is not None else element
    
    def _substitute_with_None_if_variable(self, element):
        return None if isinstance(element, Variable) else element
    
    def get_template(self):
        return ( self._substitute_with_None_if_variable(self.subject),
                 self._substitute_with_None_if_variable(self.predicate),
                 self._substitute_with_None_if_variable(self.object) )
    
    def get_variables(self):
        ret = set()
        for el in ( self.subject, self.predicate, self.object ):
            if isinstance(el, Variable):
                ret.add( el )
        return ret
    
    def n3(self):
        return "%s %s %s . \n" % (self.subject.n3(), self.predicate.n3(), self.object.n3())
    
    def __repr__(self):
        return "t(%s, %s, %s)" % ( self.subject, self.predicate, self.object )



class RESTCall(object):
    """
    Represents the REST HTTP call that a given lemma implies.
    
    A call is composed by the HTTP method, a request URI and some variables for the request body. 
    """
    
    def __init__(self, method, request_uri, var_body):
        self.method = method
        self.request_uri = request_uri
        self.var_body = Variable.create(var_body)
    
    def __repr__(self):
        return "r(m: %s, ru: %s, body: %s)" % (self.method, self.request_uri, self.var_body)
    
    def __eq__(self, other):
        return (self.method == other.method) and (self.request_uri == other.request_uri)



class Binding(object):
    """
    This class represents a binding between a variable and a value.
    """
        
    def __init__(self, variable, bound):
        self.variable = Variable.create( variable )
        self.bound = bound 
    
    @property
    def bound(self):
        return self._bound
    
    @bound.setter
    def bound(self, bound):
        self._bound = self._get_proper_bound( bound ) # should be URIRef?
    
    def _get_proper_bound(self, bound):
        ret = Variable.create(bound)
        if ret is None:
            if bound.startswith("http://"):
                ret = URIRef( bound )
            else: # TODO literal
                return bound
        return ret
    
    def __eq__(self, other_binding):
        return self.variable == other_binding.variable and self.bound == other_binding.bound

    def __hash__(self):
        return hash(self.variable) + hash(self.bound)
    
    def __repr__(self):
        return "b(var: %s, bound: %s)" % (self.variable, self.bound)


class Variable(object):
    """Class which represents ?var in a expression"""
    
    def __init__(self, name):
        self.name = name
    
    def urize(self): # could it be considered as a reification?
        return Namespaces.VAR[self.name]
    
    def fake_urize(self):
        return Namespaces.FAKE[self.name]
    
    @staticmethod
    def create(possible_var):
        """
        If 'binding_name' is "http://localhost/var#x0" or ?x0, simply takes x0.
        
        @param possible_var: can be either a 'string' or a 'rdflib.URIRef'  
        """
        prefs = (Namespaces.VAR, Namespaces.FAKE, "?")
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