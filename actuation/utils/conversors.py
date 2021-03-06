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

import re
from rdflib import XSD
from rdflib.term import Variable, Literal
from rdflib.plugins.sparql import prepareQuery
from rdflib.plugins.sparql.sparql import Query


class QueryLanguageConversor(object):
    """
    Class to convert between N3QL and SPARQL.
    """
    
    @staticmethod
    def n3ql_to_sparql( n3ql_query ):
        """
        Overly simplified conversion from N3QL to SPARQL select.
        
        N3QL pattern:
        
        @prefix p: <http://blablah> .
        ...
        {
            [sth] # this resembles to the WHERE 
        } => {
            [sth2] # this resembles to a SPARQL CONSTRUCT
        }
        
        
        It transforms to a SPARQL with the following shape:
        
        PREFIX p: <http://blablah>
        
        SELECT ?var1, ?var2 # these variables are extracted from [sth]
        WHERE {
            [sth]
        }
        """
        qlc = QueryLanguageConversor()
        qlc.parse( n3ql_query, formAt="n3ql" )
        return qlc.serialize( formAt="sparql" )

    @staticmethod
    def sparql_to_n3ql( sparql_query ):
        """
        Simplified conversion from SPARQL select to N3QL.
    
        SPARQL pattern:
        
        PREFIX p: <http://blablah>
        
        SELECT ?var1, ?var2 # these variables appear in [sth]
        WHERE {
            [sth]
        }
        
        
        It transforms to a N3QL with the following shape:
    
        {
            [sth]
        } => {
            [sth]
        }
        
        Note that it doesn't use prefixes.
        """
        qlc = QueryLanguageConversor()
        qlc.parse( sparql_query, formAt="sparql" )
        return qlc.serialize( formAt="n3ql" )
    
    def __init__(self):
        self._prefixes = {}
        self._variabs = set()
        self._premise = ""
    
    def _triple_to_n3(self, triple):
        ret = " %s %s " % ( triple[0].n3(), triple[1].n3() )
        if isinstance(triple[2], Literal):
            if triple[2].datatype == XSD.integer:
                ret += "%s" % triple[2].value
        else:
            ret += "%s" % triple[2].n3()
        return ret + " ."
    
    def parse(self, query, formAt):
        formt = formAt.lower()
        if formt=="n3ql":
            self._prefixes = N3QLParser._parse_n3ql_prefixes( query )
            self._premise = N3QLParser._extract_n3ql_uncommented_premise( query )
            self._variabs = N3QLParser._parse_n3ql_variable_names( self._premise )
        elif formt=="sparql":
            # if "query" is already a "Query" object, it's ok
            if not isinstance(query, Query):
                # if "query" is a string, build the Query object
                query = prepareQuery( query )
            self._variabs = query.algebra._vars
            self._premise = ""
            for triple in query.algebra.p['p']['triples']:
                self._premise += self._triple_to_n3( triple ) + "\n"
        else:
            raise Exception( "Query language format '%s' unsupported." % formt )
    
    def serialize(self, formAt):
        formt = formAt.lower()
        if formt=="n3ql":
            return self._to_n3ql_goal()
        elif formt=="sparql":
            return self._to_sparql_select()
        else:
            raise Exception( "Query language format '%s' unsupported." % formt )
    
    def _to_sparql_select( self ):
        if len(self._variabs)==0:
            raise Exception("The SPARQL SELECT must contain at least a variable.")
        
        ret = ""
        for name, value in self._prefixes.iteritems():
            ret += "prefix %s: <%s>\n" % (name, value) 
        
        ret += "\nselect "
        for v in self._variabs:
            ret += "?%s, " % v
        ret = ret[:-2] # remove last ", "
        ret += "\nwhere {\n"
        ret += self._premise
        ret += "}"
        return ret
    
    def _to_n3ql_goal( self ):
        if len(self._variabs)==0:
            raise Exception("The N3QL rule must contain at least a variable.")
        return "{\n%s\n} => {\n%s\n}.\n" % (self._premise, self._premise) 


class N3QLParser(object):
    
    @staticmethod
    def _parse_prefixes( n3ql_query ):
        ptt_pref = re.compile( "^\s*@prefix\s+(?P<prefix>[\w-]*)\s*:\s*<(?P<url>.*)>\s*.", re.MULTILINE | re.IGNORECASE )
        
        prefixes = {}
        for name, value in ptt_pref.findall( n3ql_query ):
            prefixes[name] = value
        return prefixes
    
    @staticmethod
    def _extract_uncommented_premise( n3ql_query ):
        ptt_premise = re.compile( "^\s*{(?P<premise>.+)}\s*=>\s*{.+}", re.MULTILINE | re.DOTALL )
        commented_premise = ptt_premise.search( n3ql_query ).group("premise")
        
        premise = ""
        for l in commented_premise.split("\n"):
            pos = l.find( "#" )
            new_line = l if pos == -1 else l[:pos]
            if new_line.strip()!="": #only adds lines with content
                premise += new_line + "\n"
        return premise
    
    @staticmethod
    def _parse_variable_names( text ):
        variabs = set()
        ptt_vars = re.compile( "\s*[?](\w+)\s+" )
        for var_name in ptt_vars.findall( text ):
            variabs.add( Variable(var_name) )
        return variabs