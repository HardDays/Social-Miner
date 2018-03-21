from abc import ABC, abstractmethod


class APostMiner(ABC):
    @abstractmethod
    def get_posts(self):
        pass
    @abstractmethod
    def to_csv(self, posts):
        pass