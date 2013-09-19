'''
Created on Sep 19, 2013

@author: tulvur
'''

from actuation.utils.files import FileUtils

class LampResource(object):
    
    def __init__(self, get_ret_file_path):
        self._get_ret_file_path = get_ret_file_path
    
    def get(self):
        return self._get_ret_file_path


class LightResource(object):
    
    # fp stands for "file path"
    def __init__(self, desc_get_fp, desc_post_fp, ret_get_tpl_fp, ret_post_tpl_fp, out_fp, init_val = 0):
        self._out_file_path = out_fp
        self._desc_get_fp = desc_get_fp
        self._desc_post_fp = desc_post_fp
        self._ret_get_tpl_fp = ret_get_tpl_fp
        self._ret_post_tpl_fp = ret_post_tpl_fp
        self._val = init_val
    
    def get(self):
        return FileUtils.generate_file_replacing(["{{value}}"], [str(self._val)], self._ret_get_tpl_fp, self._out_file_path)
    
    def post(self, post_body):
        # parse
        pass
    
    def options(self):
        return [self._desc_get_file_path, self._desc_post_file_path]