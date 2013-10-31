#! /bin/python
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
from optparse import OptionParser


PATTERNS = {
    # "@prefix : ..." ignored => I assume that it will be always needed.
    "prefix": re.compile("\s*@prefix\s+(?P<prefix>[\w-]+):(?P<url>.*)\s*.\s*"),
    "prefix_main": re.compile("\s*@prefix\s+:"),
    "empty": re.compile("^\s*$", re.MULTILINE),
    "comment": re.compile("^\s*#", re.MULTILINE),
    "prefix_use": re.compile("([\w-]+):[\w-]+[,]? ") # super error-prone (e.g. what about string literals?)
}

def remove_unused_prefixes(input_file, output_file):
    prefixes = {}
    used_prefixes = set()
    new_content = ""
    
    with open( input_file, "r" ) as inf:
        content = inf.readlines()
        
        reading_prefixes = True
        for line in content:
            if reading_prefixes:
                match = PATTERNS["prefix"].search( line )
            
                if match is None:
                    if not PATTERNS["empty"].match( line ) and not PATTERNS["comment"].match( line ) and not PATTERNS["prefix_main"].match( line ):
                        reading_prefixes = False # stop reading prefixes
                    else:
                        new_content += line
                else:
                    pref = match.group('prefix')
                    url = match.group('url')
                    prefixes[pref] = url
            
            if not reading_prefixes:
                #print prefixes
                #print line
                if not PATTERNS["empty"].match( line ) and not PATTERNS["comment"].match( line ) and not PATTERNS["prefix_main"].match( line ):
                    for match in PATTERNS["prefix_use"].findall( line ):
                        used_prefixes.add( match )
                new_content += line
            
        for up in used_prefixes:
            pline = "@prefix %s: %s .\n" % ( up, prefixes[up] )
            new_content = pline + new_content
        
        #print new_content
        with open( output_file, "w" ) as ouf:
            ouf.write( new_content )


# from rdflib import Graph
# doesn't automatically remove the unused ones!
#def remove_unused_prefixes(input_file, output_file):
#    ig = Graph()
#    ig.parse( input_file, format="n3" )
#    print ig.serialize( format="n3" )


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
		      help="Path and name of the n3 file with possible unused prefixes.")
    parser.add_option("-o", "--output", dest="output", default=None,
		      help="Path and name of the output N3 file without unused prefixes.")
    options, _ = parser.parse_args()
    
    
    outp = options.input if options.output is None else options.output
    remove_unused_prefixes( options.input, outp )