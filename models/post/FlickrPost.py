import datetime
from typing import List

from models.Point import Point
from models.post.APost import APost


class FlickrPost(APost):
    def _get_post(self):
        pass

    def get_lang(self):
        pass
    
    def __init__(self, post):
        self._post = post
        super().__init__()
    
    def __repr__(self):
        return f"Post by: {self.get_user_id()}\n" \
               f"Created at: {self.get_creation_time()}\n" \
               f"Coordinates: ({self.get_point().latitude}, {self.get_point().longitude})\n" \
               f"Tags: {self.get_tags()}\n" \
               f"Description: {self.get_text()}\n" \
               f"URL: {self.get_photo_url()}"
    
    def get_tags(self) -> List[str]:
        try:
            return self._post['tags'].split(' ')
        except Exception as e:
            return []
    
    def get_text(self) -> str:
        text = ''
        try:
            text += self._post['title']
            text += self._post['description']['_content']
        except Exception as e:
            pass
        return text
    
    def _extract_point(self) -> Point:
        return Point(float(self._post['latitude']), float(self._post['longitude']))
    
    def get_creation_time(self) -> int:
        return int(self._post['dateupload'])
    
    def get_user_id(self) -> str:
        return self._post.get('owner')
    
    def get_photo_url(self) -> str:
        return self._post.get('url_o', '')
    
    def for_df(self):
        """
        Prepares data to be put in Dataframe with columns:
            'coordinates',
            'text',
            'tags',
            'creation_time',
            'user_id',
            'photo_url'
            'post'
        :return:
        """
        return self._point.get_tuple(), \
               self.get_text(), \
               self.get_tags(), \
               self.get_creation_time(), \
               self.get_user_id(), \
               self.get_photo_url(), \
               self._get_post()