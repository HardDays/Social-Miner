from typing import List
from models.Point import Point
from time import mktime

from models.post.APost import APost


class Tweet(APost):
    def __init__(self, tweet, point: Point):
        self._tweet = tweet
        self._point = point
        super().__init__()
    
    def __repr__(self):
        return "\n%s\n[%s]\n%s\n" % (self._tweet.text, " ".join(self.get_tags()), self._tweet.created_at)
    
    def get_tags(self) -> List[str]:
        return [h.get('text', '') for h in self._tweet.entities.get('hashtags', [])]
    
    def get_text(self) -> str:
        return self._tweet.text
    
    def get_creation_time(self) -> float:
        """
        Time of models creation
        :return: timestamp
        """
        return mktime(self._tweet.created_at.timetuple())
    
    def get_point(self) -> Point:
        return self._point
    
    def get_photo(self):
        if 'retweeted_status' in self._tweet._json.keys():
            return self._tweet.retweeted_status.quoted_status['entities']['media'][0]['media_url']
        else:
            return None
    
    def get_lang(self):
        return self._tweet.metadata.get('iso_language_code', '')
    
    def get_user_id(self):
        return self._tweet._json.get('user').get('id')

    def _get_post(self):
        return self._tweet

    def _extract_point(self):
        if self._tweet.coordinates:
            coord = self._tweet.coordinates.get('coordinates', None)
            self._point = Point(float(coord[1]), float(coord[0]))
        return self._point