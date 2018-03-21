import flickrapi
import time
import datetime

from models.Point import Point
from models.post.FlickrPost import FlickrPost


class FlickrProvider():
    def __init__(self):
        api_key = '044d2fe47fdd01af9a8230da3e38fac4'
        api_secret = 'b0b4c597a87c18ed'
        
        self.flickr = flickrapi.FlickrAPI(api_key, api_secret, format='parsed-json')
        self.flickr.authenticate_via_browser(perms='read')

    def get_posts(self, point: Point, radius=32,min_pos_date=0.0, max_pos_date=0.0, min_taken_date=0.0,
                  max_taken_date=0.0):
        if not max_pos_date:
            max_pos_date = self._to_flickr_date(datetime.datetime.timestamp(datetime.datetime.today()))
        if not max_taken_date:
            max_taken_date = max_pos_date
        if not min_pos_date:
            min_pos_date = '2018-03-20 00:00:00'
        if radius > 32: radius = 32
        params = {
            'q': ' ',
            'has_geo': 1,  # to search only for photos which has geo coordinates
            'geo_context': 0,
            'lat': point.latitude,
            'lon': point.longitude,
            'radius': radius,
            'radius_units': 'km',
            'min_taken_date': min_taken_date,
            'max_taken_date': max_taken_date,
            'min_upload_date': min_pos_date,
            'max_upload_date': max_pos_date,
            'extras': 'date_upload, description, geo, tags, machine_tags, url_o',
            'per_page': 20,
            'page': 1
        }
    
        ph = self.flickr.photos.search(**params)
        photos = [self.make_post(photo) for photo in ph['photos']['photo']]
        for params['page'] in range(2, ph['photos']['pages'] + 1):
            photos.extend([self.make_post(photo) for photo in self.flickr.photos.search(**params)['photos']['photo']])
        return photos

    def make_post(self, photo):
        if not photo.get('url_o', ''):
            params = {
                'photo_id': photo['id']
            }
            photo['url_o'] = self.flickr.photos.getSizes(**params).get('sizes', {}).get('size', [{}])[-1].get('source',
                                                                                                              '')
        return FlickrPost(photo)

    def _to_flickr_date(self, timestamp: float) -> str:
        try:
            return str(datetime.datetime.fromtimestamp(timestamp)).split('.')[0]
        except Exception as e:
            return '2017-12-31 00:00:00'