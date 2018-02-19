import datetime
from typing import List

from models.post.APost import APost
from models.Point import Point


class VKPost(APost):

    def get_lang(self):
        # TODO
        return ""

    def __init__(self, post):
        self._post = post
        super().__init__()

    def __repr__(self):
        return "\n%s\n[%s]\nCreated at: %s\n" % \
               (self.get_text(), " ".join(self.get_tags()),
                datetime.datetime.fromtimestamp(int(self.get_creation_time())))

    def get_tags(self) -> List[str]:
        return [t[1:] for t in self.get_text().split(' ') if '#' in t]

    def get_text(self) -> str:
        return self._post['text_helpers']

    def _extract_point(self) -> Point:
        coord = self._post['venue']['coordinates'].split(' ')
        return Point(float(coord[0]), float(coord[1]))

    def get_creation_time(self) -> float:
        return self._post['date']
    
    def get_user_id(self):
        return self._post.get('owner_id', 0)

    def _get_post(self):
        return self._post