'''
Created on Sep 19, 2013

@author: tulvur
'''

from actuation.api.light_rest import LightProviderREST

class LightProviderRESTMock(LightProviderREST):
    
    def __init__(self, lamp_resource, light_resource):
        super(LightProviderREST,self).__init__(lamp_resource, light_resource)
    
    # In the mock implementation, the resources are not retrieved through HTTP
    
    @property
    def lamp_resource(self):
        return self._lamp_resource
        
    @property
    def light_resource(self):
        return self._light_resource