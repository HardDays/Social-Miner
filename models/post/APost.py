from typing import List
from abc import ABC, abstractmethod
from models.Point import Point


class APost(ABC):
    """
    Social Media Post
    Abstract entity, e.g. tweet, fb models, vk models etc.
    """
    
    def __init__(self):
        self._point = self._extract_point()
    
    @abstractmethod
    def get_text(self) -> str:
        pass
    
    def get_point(self) -> Point:
        return self._point
    
    @abstractmethod
    def get_creation_time(self) -> float:
        """
        Time of models creation
        :return: timestamp
        """
        pass
    
    @abstractmethod
    def get_tags(self) -> List[str]:
        pass
    
    @abstractmethod
    def _extract_point(self) -> Point:
        pass
    
    @abstractmethod
    def get_user_id(self):
        pass

    @abstractmethod
    def _get_post(self):
        pass

    @abstractmethod
    def get_lang(self):
        pass
    
    @abstractmethod
    def for_df(self):
        pass

    def to_dict(self):
        return {
            'text_helpers': self.get_text(),
            'point': {
                'lat': self.get_point().latitude,
                'lng': self.get_point().longitude
            },
            'time': self.get_creation_time(),
            'places_tags': self.get_tags()
        }

