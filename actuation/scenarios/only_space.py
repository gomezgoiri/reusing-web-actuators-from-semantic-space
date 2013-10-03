from actuation.scenarios.abstract import AbstractSimulation, main
from actuation.impl.space import CoordinationSpace
from actuation.impl.space.lamp.mock.provider import LampProviderSpaceMock
from actuation.impl.space.lamp.mock.consumer import LampConsumerSpaceMock


class OnlySpaceBasedDevicesSimulator(AbstractSimulation):
    
    def __init__(self, input_folder, output_folder, path_to_reasoner):
        super(OnlySpaceBasedDevicesSimulator, self).__init__( output_folder )
        self.input_folder = input_folder
    
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
        self.space = CoordinationSpace("onlySpace")
        
        debug = True
        self.lp = LampProviderSpaceMock( self.space, self.input_folder, self.output_folder, debug = debug )
        self.lc = LampConsumerSpaceMock( self.space, self.input_folder, self.output_folder, debug = debug )
    
    def execute(self):
        '''
        Executes the scenario where the consumer tries to change the light in the environment.
        '''
        self.lp.subscribe_task()
        # do sth
        self.lc.write_task()
    
    def check(self):
        return False


if __name__ == '__main__':
    main( OnlySpaceBasedDevicesSimulator )