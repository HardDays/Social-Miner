from typing import *
from models.post.APost import APost
from models.Point import Point
from abc import ABC, abstractmethod


class PostProvider(ABC):
    """
    Abstract models provider
    """
    @abstractmethod
    def get_posts(self, point: Point, radius: int, lang: str, wo_coords: bool, count=-1, from_data="", to_data=""):
        """
        Abstract method that every provider must Override.
        Returns ALL posts near given point.
        """
        pass