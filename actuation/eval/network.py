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

from actuation.eval.charts.diagram import DiagramGenerator

class RESTRequests(object):
    
    def __init__(self, num_nodes_list, resources_per_provider, requests_to_activate):
        self.num_nodes_list = num_nodes_list # This must be a list
        # those really needed are only the resources per request in the activation plan
        self.resources_per_provider = resources_per_provider
        self.requests_to_activate = requests_to_activate
    
    def get_requests(self):
        ret = []
        for num_nodes in self.num_nodes_list:
            ret.append( num_nodes * self.resources_per_provider + self.requests_to_activate )
        return ret


class SpaceRequests(object):
    
    def __init__(self, num_nodes_list, written_graphs_per_provider):
        self.num_nodes_list = num_nodes_list
        self.written_graphs_per_provider = written_graphs_per_provider
        # self.nodes_involved = 2
        self.requests_to_activate = {}
        self.requests_to_activate['per_consumer'] = 3 # write task, subscribe to result, read result 
        self.requests_to_activate['per_provider'] = 2 # (subscribe to task already counted below), read task, write result
        self.requests_to_activate['per_space'] = 2 # notification on task, notification on result
    
    def get_requests(self):
        ret = []
        for num_nodes in self.num_nodes_list:
            total = num_nodes * (1 + self.written_graphs_per_provider) # subscribe to task
            # TODO actually, the nodes write their content into the space too
            for val in self.requests_to_activate.values():
                total += val
            ret.append(total)
        return ret


if __name__ == '__main__':
    rng = range(0, 1001, 100)
    rng[0] = 1
    
    rest = RESTRequests( rng,
                        5, # One for each OPTIONS and GET verb of each resource,
                           # supposing that they only provide one measure at a time.
                           # /lamp (GET), /lamp/actuators (GET), /lamp/actuators/light (GET, OPTIONS), /lamp/actuators/light/01 (GET)

                            # Anyway, this can be improved redesigning the API
                        2 ) # The actuation in our scenario is composed by two requests
    space = SpaceRequests( rng,
                           2 )  # In our scenario, the provider writes 2 graphs: lamp description, bulb light description
                                # But this depends
    
    data = {}
    data['rest'] = {}
    data['rest']['num_nodes'] = rng
    data['rest']['requests'] = rest.get_requests()
    data['space'] = {}
    data['space']['num_nodes'] = rng
    data['space']['requests'] = space.get_requests()
    
    print data
    d = DiagramGenerator("Network usage by strategies", data, ylabel_name="Requests")
    d.save('/tmp/requests_by_techniques.svg')