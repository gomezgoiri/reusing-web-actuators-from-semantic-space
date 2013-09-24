from optparse import OptionParser
from actuation.scenarios.abstract import AbstractSimulation
from actuation.utils.files import append_slash_if_absent
from actuation.impl.mock.lamp_rest_provider import LampProviderRESTMock
from actuation.impl.mock.lamp_rest_consumer import LampConsumerRESTMock


class OnlyRESTDevicesSimulator(AbstractSimulation):
    
    def __init__(self, input_folder, output_folder, reasoner):
        super(OnlyRESTDevicesSimulator, self).__init__( output_folder )
        self.input_folder = input_folder
        self.reasoner = reasoner
    
    @property    
    def lc(self):
        return self.nodes["consumer"]
    
    @lc.setter
    def lc(self, value):
        self.nodes["consumer"] = value
    
    @property    
    def lp(self):
        return self.nodes["provider"]
    
    @lp.setter
    def lp(self, value):
        self.nodes["provider"] = value
    
    def configure(self):
        self.lp = LampProviderRESTMock( self.input_folder, self.output_folder )
        self.lc = LampConsumerRESTMock( self.output_folder, self.reasoner)
        self.lc.discover( self.lp )
        print self.lp.get_resource("/lamp/light").get()
    
    def execute(self):
        '''
        Executes the scenario where the consumer tries to change the light in the environment.
        '''
        # do sth
        pass
    
    def check(self):
        pass


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-i", "--input", dest="input",
                      help="Base directory where all the files used in the simulation are stored.")
    parser.add_option("-o", "--output", dest="output", default="/tmp",
                      help="Output folder where the processed results will be written.")
    parser.add_option("-e", "--euler", dest = "euler", default='../../../../',
                      help = "Path to Euler.jar")
    parser.add_option("-c", "--clean", dest = "clean", default="True",
                      help = "Specifies whether the output directory should be clean after the execution.")
    (options, args) = parser.parse_args()
    
    from actuation.proofs.reasoner import EulerReasoner
    reasoner = EulerReasoner( options.euler )
    
    sim = OnlyRESTDevicesSimulator( append_slash_if_absent( options.input ),
                                    append_slash_if_absent( options.output ),
                                    reasoner )
    
    sim.run()
    
    if options.clean.lower() == "true":
        sim.clean()