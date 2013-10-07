'''
Created on Oct 7, 2013

@author: tulvur
'''

import re
from actuation.api.discovery import AbstractDiscovery


class MockDiscovery(AbstractDiscovery):
    
    def __init__(self):
        super(MockDiscovery, self).__init__()
        self._nodes = {}
    
    def add_discovered(self, node, address):
        self._nodes[address] = node
    
    # In the mock implementation, the resources are not retrieved through HTTP
    def get_node(self, url_address):
        """
        @param url_address: An http address to a certain resource.
                            E.g. "http://node.deusto.es/lamp/light"
        @return: If no node is found for this address, it returns None.
                Otherwise, it returns a tuple containing the node and the rest of the address.
                E.g. providing "node.deusto.es" corresponds to nodeN: (nodeN, "lamp/light")
                
        """
        pat = re.compile("http://(?P<address>[\.\w]+)(?P<remaining>.*)")
        match = pat.search( url_address )
        if match:
            addr = match.group('address')
            if addr in self._nodes:
                remaining = match.group('remaining')
                return (self._nodes[ addr ], remaining)
        # else returns None
    
    def get_nodes(self):
        return self._nodes.itervalues()
        # else returns None