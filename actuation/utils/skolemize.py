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
from rdflib import Graph
from StringIO import StringIO
from actuation.proofs import Namespaces


def _fix_the_serialized_mess( n3_serialization_prefixes_everywhere ):
    by_lines = n3_serialization_prefixes_everywhere.split('\n')
    
    prefexp = re.compile(r"@prefix( \w*): <(.+)>\s*.")
    pretty_n3_serialization = ""
    prefixes = set()
    for line in by_lines:
        ls = line.lstrip()
        if ls.startswith("@prefix"):
            for p in prefexp.findall( ls ):
                prefixes.add( p )
        else:
            indx = ls.find("@prefix") # quick and dirty => if it is inside a string, bad luck :-P
            if indx != -1:
                ls = ls[:indx] # supress the last part
            pretty_n3_serialization += ls + "\n"
    
    pretty_n3_serialization = "\n\n" + pretty_n3_serialization
    
    for p in prefixes:
        pretty_n3_serialization = "@prefix%s: <%s> .\n" % (p[0], p[1]) + pretty_n3_serialization;
    
    return pretty_n3_serialization


# http://answers.semanticweb.com/questions/8336/what-is-skolemization
def skolemize_less_optimum(input_file, output_file):
    g = Graph()
    g.parse( input_file, format="n3" )
    g2 = g.skolemize() # str(Namespaces.FAKE) )
    # In 4.0.1 this throws an error: https://github.com/RDFLib/rdflib/commit/f5da2a2aca054748877aa7c6d722dc087472a858
    # Until a new version is uploaded: pip install https://github.com/RDFLib/rdflib/tarball/master
    #g2.serialize( filename+".bak", format="n3" ) # awful serialization!
    #print g2.serialize( format="n3")
    prefixes_everywhere = g2.serialize( format="n3" ) # awful serialization!
    serial = _fix_the_serialized_mess( prefixes_everywhere )
    with open (output_file, "w") as output_file:
        output_file.write( serial )


# Or much more straightforward and fast alternative... :-S
def skolemize_lemmas(input_file, output_file):
    fake_prefix = r"@prefix fake: <%s>." % Namespaces.FAKE
    with open (input_file, "r") as input_file:
        data = re.sub('_:lemma(?P<num>\d+)', 'fake:lemma\g<num>', input_file.read())
        g = Graph()
        g.parse( StringIO( fake_prefix + "\n" + data ), format="n3" )
        with open(output_file, "w") as output_file:
            output_file.write( fake_prefix + "\n" + data)