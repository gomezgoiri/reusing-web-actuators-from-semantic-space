from abc import ABCMeta, abstractmethod


class Node(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def start(self):
        pass
    
    @abstractmethod
    def stop(self):
        pass