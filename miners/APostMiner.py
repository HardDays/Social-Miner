from abc import ABC, abstractmethod


class APostMiner(ABC):
    
    @abstractmethod
    def to_csv(self, posts):
        pass
