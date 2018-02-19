import time
from typing import List

import vk
from providers.PostProvider import PostProvider
from models.post.VKPost import VKPost

from models.post.APost import APost
from models.Point import Point


class VKProvider(PostProvider):
    access_token = 'a44133d9502daeaac0e212b1cca6519e7dfe1ae1d39135f22f48d9c4191954ad868ac0673a554f69c1b0c'

    def __init__(self):
        self.vk_api = vk.API(vk.Session(access_token=self.access_token))

    def get_posts(self, point: Point, radius=50, lang='en', wo_coords=False, count=0):
        q = ' '
        limit = 200  # VK limit
        min_date = 951858000.0  # datetime.datetime(2000,3,1,0,0).timestamp()
        max_date = time.time()
        
        if not count:
            batch = True
        else:
            batch = False
            if limit > count: limit = count
        
        params = {
            'q': q,
            'count': limit,
            'latitude': self._to_vk_point(point.latitude),
            'longitude': self._to_vk_point(point.longitude),
            'start_time': int(min_date),
            'end_time': int(max_date)  # float("%.0f" % max_date)
        }
        
        feed = []
        try:
            res = self.vk_api.newsfeed.search(**params)
            feed = [VKPost(r) for r in res[1:]]
            if batch:
                count = int(res[0])  # number of pages
            for _ in range(limit, count, limit):
                params['start_from'] = res['next_from']
                res = self.vk_api.newsfeed.search(**params)
                feed.extend([VKPost(r) for r in res[1:]])
        except Exception as e:
            print(f"EXEPTION: {e}")
        return feed
    
    def _to_vk_point(self, point):
        return float("%.3f" % point)
