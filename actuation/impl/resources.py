'''
Created on Sep 19, 2013

@author: tulvur
'''

import tempfile
from jinja2 import Template


class Resource(object):
    
    def __init__(self):
        super(Resource, self).__init__()
        self.sub_resources = {} # key: subpath, value: resource_object

    def add_sub_resource(self, path, resource):
        self.sub_resources[path] = resource
    
    def _returnIfExists(self, resource_name, remaining_path):
        if resource_name in self.sub_resources: # usual case
            if remaining_path == "":
                return self.sub_resources[ resource_name ]
            else:
                return self.sub_resources[ resource_name ].get_sub_resource( remaining_path )
    
    def _join_strings_in_path(self, strings):
        if not strings: # empty
            return ""
        else:
            ret = ""
            for i in range( len(strings) ): # from 0 to N
                if ret == "": # first occurrence (or i==0)
                    ret = strings[i]
                else:
                    ret += "/" + strings[i]
            return ret
    
    def get_sub_resource(self, path):
        '''Path comes without the initial slash (e.g. bar/foo).'''
        # Maybe foo is not a sub_resource but foo/bar is
        parts = path.split("/")
        
        for i in range( len(parts) ): # from 0 to N
            resource_name = self._join_strings_in_path( parts[ : i+1 ] )
            remaining = self._join_strings_in_path( parts[ i+1 : len(parts) ] )            
            ret = self._returnIfExists(resource_name, remaining)
            if ret is not None:
                return ret
        return None
    
    def get_all_resources(self):
        ret = []
        for res in self.sub_resources.itervalues():
            ret.append( res )
            ret.extend( res.get_all_resources() )
        return ret
    
    def get_sub_resource_paths(self):
        return self.sub_resources.iterkeys()


class LampResource(Resource):
    
    def __init__(self, input_folder):
        super(LampResource, self).__init__()
        self._get_ret_file_path = input_folder + "lamp_ret.n3"
    
    def get(self):
        return self._get_ret_file_path


class LightResource(Resource):
    
    # fp stands for "file path"
    def __init__(self, input_folder, out_fp, init_val = 0):
        super(LightResource, self).__init__()
                                        
        self.ret_tpl_fp = input_folder + "light_ret.n3.tpl"
        self._desc_post_fp = input_folder + "light_descpost.n3"
        self._desc_get_fp = input_folder + "measure_descget.n3"
        
        self.filepath = out_fp + "light.n3"
        
        self.measure_factory = LightMeasureResourceFactory( self._desc_get_fp,
                                                            input_folder + "measure_ret.n3.tpl",
                                                            out_fp )
        self._add_measure( init_val )
    
    def _add_measure(self, light_val):
        measure_rsc = self.measure_factory.create( light_val )
        self.add_sub_resource( str( measure_rsc.id ), measure_rsc )
        return measure_rsc
    
    def _get_measures_ids(self):
        return self.get_sub_resource_paths()
    
    def _update_file(self):
        with open( self.ret_tpl_fp, "r" ) as input_file:
            with open( self.filepath, "w" ) as output_file:
                template = Template( input_file.read() )
                outc = template.render( measures = self._get_measures_ids() )
                output_file.write( outc )
    
    def get(self):
        self._update_file()
        return self.filepath
    
    def post(self, post_body):
        # post_body is a Literal
        measure_rsc = self._add_measure( post_body.value )
        return measure_rsc.get()
    
    # GET /measure/XX not particular of a "measure" instance --> we share it ALSO in the parent
    def options(self):
        return [self._desc_post_fp, self._desc_get_fp]


class LightMeasureResourceFactory(object):
    
    # fp stands for "file path"
    def __init__(self, desc_get_fp, ret_tpl_fp, out_fp):
        self._out_file_path = out_fp
        self._desc_get_fp = desc_get_fp
        self.ret_tpl_fp = ret_tpl_fp
        self.counter = 0
    
    def create(self, light_value):
        self.counter += 1
        return LightMeasureResource( self.counter,
                                     self._desc_get_fp,
                                     self.ret_tpl_fp,
                                     self._out_file_path,
                                     light_value )


class LightMeasureResource(Resource):
    
    # fp stands for "file path"
    def __init__(self, iid, desc_get_fp, ret_tpl_fp, out_fp, value = 0):
        super(LightMeasureResource, self).__init__()
        self.id = iid
        self._val = value
        
        self._desc_get_fp = desc_get_fp
        
        self.ret_filepath = None
        self._generate_ret( ret_tpl_fp, out_fp )
    
    def _generate_ret(self, ret_tpl_fp, output_folder):
        _, self.ret_filepath = tempfile.mkstemp( dir = output_folder, suffix=".n3" )
        with open( ret_tpl_fp, "r" ) as input_file:
            with open( self.ret_filepath, "w" ) as output_file:
                template = Template( input_file.read() )
                outc = template.render( id = self.id, value = self._val )
                output_file.write( outc )
    
    def get(self):
        return self.ret_filepath
    
    def options(self):
        return [self._desc_get_fp]