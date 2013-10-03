'''
Created on Sep 19, 2013

@author: tulvur
'''

from tempfile import mkdtemp
from shutil import rmtree
from optparse import OptionParser
from abc import ABCMeta, abstractmethod
from actuation.utils.files import append_slash_if_absent

class AbstractSimulation(object):
    
    __metaclass__ = ABCMeta
    
    
    def __init__(self, output_folder):
        self.nodes = {}
        self.output_folder = mkdtemp( dir = output_folder ) + "/"
    
    # new possible phase
    # def initialize(self):  
    
    def run(self):
        '''
        Runs the scenario where the consumer tries to change the light in the environment.
        '''
        self.configure()
        
        for node in self.nodes.itervalues():
            node.start()
        
        self.execute()
        
        for node in self.nodes.itervalues():
            node.stop()
        
        if self.check():
            print "The scenario behaved as expected."
        else:
            print "The scenario didn't run as expected."
    
    @abstractmethod
    def configure(self):
        pass
    
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def check(self):
        pass
    
    def clean(self):
        rmtree( self.output_folder )


def main( simulation_subclass ):
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="Base directory where all the files used in the simulation are stored.")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default=None,
                      help = "Path to Euler.jar")
    parser.add_option("-c", "--clean", dest = "clean", default="True",
                      help = "Specifies whether the output directory should be clean after the execution.")
    options, _ = parser.parse_args()
    
    sim = simulation_subclass( append_slash_if_absent( options.input ),
                            append_slash_if_absent( options.output ),
                            # optional, not all the simulations will have it!
                            None if options.euler is None else append_slash_if_absent( options.euler ) )
    
    sim.run()
    
    if options.clean.lower() == "true":
        sim.clean()