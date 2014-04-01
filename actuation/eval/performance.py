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

import json
from optparse import OptionParser
from actuation.eval.charts.diagram import DiagramGenerator
from actuation.scenarios.only_rest import OnlyRESTDevicesSimulator
from actuation.scenarios.only_space import OnlySpaceBasedDevicesSimulator
from actuation.utils.files import append_slash_if_absent


class PerformanceChecker(object):
    
    def __init__(self, range_providers, simulation_subclass, innput, output, reasoner_path, repetitions=1, clean=False, debug=False):
        # list with list for each repetition in an execution for a given number of providers
        self.range_providers = range_providers
        self.simulation_subclass = simulation_subclass
        self.input = innput
        self.output = output
        self.reasoner_path = reasoner_path
        self.repetitions = repetitions
        self.clean = clean
        self.debug = debug
    
    def run(self):
        self.time_measures = []
        for num_nodes in self.range_providers:
            time_needed = []
            for _ in range(self.repetitions):
                sim = self.simulation_subclass( self.input,
                                                self.output,
                                            # optional, not all the simulations will have it!
                                            self.reasoner_path, # we do not expect a path there anymore
                                            num_nodes,
                                            self.debug )
                sim.run()
                time_needed.append( sim.execution_time ) # to also consider the loading time: + sim.starting_time
                if self.clean: sim.clean()
            self.time_measures.append(time_needed)
            
    
    def get_results(self):
        data = {}
        data['num_nodes'] = self.range_providers
        data['requests'] = self.time_measures
        return data


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-n", "--nRep", dest="repetitions", type="int", default=1,
                      help="Number of repetitions for each execution.")
    parser.add_option("-i", "--input", dest="input",
                      help="Base directory where all the files used in the simulation are stored.")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default="/opt/eye/bin/eye.sh",
                      help = "Path to the EYE reasoner. E.g., '/opt/eye/bin/eye.sh'.")
    parser.add_option("-c", "--clean", dest = "clean", default="False",
                      help = "Specifies whether the output directory should be clean after the execution.")
    parser.add_option("-d", "--debug", dest = "debug", default="False",
                      help = "Generate messages and files to check afterwards.")
    options, _ = parser.parse_args()
    
    innput = append_slash_if_absent(options.input)
    output = append_slash_if_absent(options.output)
    
    data = {}
    #rng = range(0, 1001, 200)
    #rng = range(400, 801, 100)
    # In the REST test, it seem to have a linear progression as more semantic content is handled,
    # but then, at certain intervals, it take much longer than expected:
    #     + 500 to 800 (in all the executions: 550, 600, 700 and 750)
    #     + from 1000 to ? (problems deteced on the executions for 1100 and 1200)
    #rng = range(0, 501, 50) + range(800, 1001, 50)
    #rng[0] = 1
    rng = [1,500, 600, 700, 800, 900]
    
    simRest = PerformanceChecker(
                        rng, OnlyRESTDevicesSimulator, innput + "rest/",
                        output, options.euler, options.repetitions,
                        options.clean.lower() == "true" )
    simRest.run()
    
    simSpace = PerformanceChecker(
                        rng, OnlySpaceBasedDevicesSimulator, innput + "space/",
                        output, options.euler, options.repetitions,
                        clean = (options.clean.lower() == "true") )
    simSpace.run()
    
    data = {}
    data['rest'] = {}
    data['rest'] = simRest.get_results()
    data['space'] = {}
    data['space'] = simSpace.get_results();
    
    # Write results in Json format
    ofilename = output + "results.json"
    with open(ofilename, "w") as ofile:
        ofile.write( json.dumps( data ) )
        
    #print data
    #d = DiagramGenerator("Performance of two of the strategies as it varies with the scale", data)
    #d.save('/tmp/performance_by_strategies.pdf')