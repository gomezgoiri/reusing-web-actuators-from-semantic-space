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
import tempfile
#from actuation.utils.files import append_slash_if_absent

def append_slash_if_absent( file_path ):
    return file_path if file_path.endswith( "/" ) else file_path + "/"


class FileUtils(object):
    
    @staticmethod
    def generate_file_replacing(patterns, replacements, input_file_path, output_folder, output_filename=None):
        #file_handle = None
        file_pathname = None
        
        output_folder = append_slash_if_absent( output_folder )
        
        if output_filename is None:
            # returns a tuple containing an OS-level handle to an open file (as would be returned by os.open())
            # and the absolute pathname of that file, in that order.
            _, file_pathname = tempfile.mkstemp( dir = output_folder, suffix=".n3" )
            # "_" is not a file descriptor, it is an int! :-S
        else:
            file_pathname = output_folder + output_filename
        
        with open( input_file_path, "r" ) as input_file:
            with open( file_pathname, "w" ) as output_file:
                data = input_file.read()
                for pat, rep in zip(patterns, replacements):
                    data = re.sub(pat, rep, data)
                output_file.write(data)
        
        
        return file_pathname