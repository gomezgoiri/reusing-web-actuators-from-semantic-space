'''
Created on Sep 20, 2013

@author: tulvur
'''

from actuation.api.light_rest import RESTProvider, LightConsumerREST

class LightConsumerRESTMock(LightConsumerREST):
    
    def __init__(self):
        super(LightConsumerRESTMock,self).__init__()
        self.nodes = []
        self.descriptions = []
    
    # In the mock implementation, the resources are not retrieved through HTTP
    
    def discover(self, node):
        self.nodes.append( node )  
    
    def _obtain_resource_descriptions(self):
        for node in self.nodes:
            if isinstance(node, RESTProvider):
                for resource in node.resources.itervalues():
                    if hasattr(resource, 'options'): # maybe it does not implement it
                        opts = resource.options()
                        if hasattr(opts, '__iter__'):
                            self.descriptions.extend( resource.options() )
                        else:
                            self.descriptions.append( resource.options() )
    
    def start(self):
        self._obtain_resource_descriptions()
    
    def stop(self):
        pass