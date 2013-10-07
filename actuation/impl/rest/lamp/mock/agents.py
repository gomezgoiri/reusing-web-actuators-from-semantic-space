from actuation.api.rest import RESTProvider


class Crawler(object):
    
    def __init__(self, input_folder, discovery):
        self.discovery = discovery
        self._descriptions = set()
        self._base_knowledge = set()
        self.preference_file = input_folder + "additional_info.n3"
    
    # or directly update in the constructor
    def update(self):
        self._obtain_resource_descriptions()
        self._obtain_base_knowledge()
    
    def _obtain_resource_descriptions(self):
        for node in self.discovery.get_nodes():
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'options'): # maybe it does not implement it
                        opts = resource.options()
                        if hasattr(opts, '__iter__'):
                            self._descriptions.update( opts ) # == extend in lists
                        else:
                            self._descriptions.add( opts ) # == append in lists
     
    def _obtain_base_knowledge(self):
        '''Crawling to obtain base knowledge (done by an spider, autonomous agent)'''
        for node in self.discovery.get_nodes():
            if isinstance(node, RESTProvider):
                # In the real implementation the resources must be discovered using HTTP
                for resource in node.get_all_resources():
                    if hasattr(resource, 'get'): # maybe it does not implement it
                        opts = resource.get()
                        self._base_knowledge.add( opts ) # == append in lists
        self._base_knowledge.add( self.preference_file )
    
    @property
    def descriptions(self):
        return self._descriptions
    
    @property
    def base_knowledge(self):
        return self._base_knowledge