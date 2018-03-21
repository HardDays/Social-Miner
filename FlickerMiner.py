from models.Point import Point
from providers.FlickrProvider import FlickrProvider
import pandas as pd


class FlickerMiner:
    def __init__(self):
        self.provider = FlickrProvider()
    
    def get_posts(self, point: Point, radius=32, min_pos_date=0.0, max_pos_date=0.0, min_taken_date=0.0,
                  max_taken_date=0.0):
        return self.provider.get_posts(point, radius, min_pos_date, max_pos_date, min_taken_date, max_taken_date)

    def to_csv(self, posts, date_from, date_to, name=''):
        df = pd.DataFrame(columns=['coordinates',
                                   'text',
                                   'tags',
                                   'creation_time',
                                   'user_id',
                                   'photo_url'
                                   'post'])
    
        for i, post in enumerate(posts):
            df.loc[i] = post.for_df()
    
        df.to_csv(f"posts/flickr/{name}_{date_from}_{date_to}.csv",
                  encoding='utf-8')
      
        
m = FlickerMiner()
posts = m.get_posts(Point(41.383333, 2.183333))
for post in posts[:5]:
    print(post.__repr__())