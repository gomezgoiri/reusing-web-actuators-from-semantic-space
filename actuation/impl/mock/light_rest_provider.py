'''
Created on Sep 19, 2013

@author: tulvur
'''

from actuation.api.light_rest import LightProviderREST

class LightProviderRESTMock(LightProviderREST):
    
    def __init__(self, lamp_resource, light_resource):
        super(LightProviderRESTMock,self).__init__(lamp_resource, light_resource)
    
    # In the mock implementation, the resources are not retrieved through HTTP
    
    def get_resource(self, url):
        return self.resources[url]
    
    def start(self):
        pass
    
    def stop(self):
        pass