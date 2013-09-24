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
from actuation.proofs.interpretation.variable import fake_ns


# TODO Damn it, I should have used Node.skolemize(authority='http://rdlib.net/') !
# Otherwise BIG TODO => use FileUtils!
def unblank_lemmas(input_file_path, output_file_path):
    fake_prefix = r"@prefix fake: <%s>." % fake_ns
    with open (input_file_path, "r") as input_file:
        data = re.sub('_:lemma(?P<num>\d+)', 'fake:lemma\g<num>', input_file.read())
        # Or...
        # g = Graph()
        # g.parse( StringIO( fake_prefix + "\n" + data ), format="n3" )
        # print g.serialize(format="n3")
        with open (output_file_path, "w") as output_file:
            output_file.write( fake_prefix + "\n" + data)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="File to process")
    parser.add_option("-o", "--output", dest="output", default="/tmp/unblanked.n3",
                      help="Processed file")
    (options, args) = parser.parse_args()
    
    unblank_lemmas(options.input, options.output)