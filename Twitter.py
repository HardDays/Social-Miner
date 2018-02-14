import tweepy
import time
import pandas as pd
from typing import *
import datetime


mari_credentials = {
    "api_key": "7gIWHgOmLgzJQ12z2gUfnyzFK",
    "api_secret": "sAlVoKi3fHTRkygSaQWea20tDcPYkklwgghySZoB3Y8XAZgsDK",
    "access_token": "3015306009-7S3Kj3qEBHburQ4bMQq1cEIpluXN8CasjTvMfGB",
    "access_token_secret": "zzqHVQFTzd820xtvBwgG3CpkOLr38KwWSK16xRpaNPh9w",
}
vlad_credentials = {
    "api_key": "1adwVKJCXmHauYAl3qSiYWb4h",
    "api_secret": "La15fOJqldGVTxPUH51Ex3s2ouSCrVQVsI2rFUSOKTyUr9D8uG",
    "access_token": "853328235505094656-WzbO8uA9RIM2DyNRd6qtWKorefCUXBC",
    "access_token_secret": "HyzQlC5Z3iHYmidAH1DS6V3t2yMGT9SgwgDPGXddXF3D7",
}

credentials = [{
    "api_key": "7gIWHgOmLgzJQ12z2gUfnyzFK",
    "api_secret": "sAlVoKi3fHTRkygSaQWea20tDcPYkklwgghySZoB3Y8XAZgsDK",
    "access_token": "3015306009-7S3Kj3qEBHburQ4bMQq1cEIpluXN8CasjTvMfGB",
    "access_token_secret": "zzqHVQFTzd820xtvBwgG3CpkOLr38KwWSK16xRpaNPh9w",
}, {
    "api_key": "1adwVKJCXmHauYAl3qSiYWb4h",
    "api_secret": "La15fOJqldGVTxPUH51Ex3s2ouSCrVQVsI2rFUSOKTyUr9D8uG",
    "access_token": "853328235505094656-WzbO8uA9RIM2DyNRd6qtWKorefCUXBC",
    "access_token_secret": "HyzQlC5Z3iHYmidAH1DS6V3t2yMGT9SgwgDPGXddXF3D7",
}]


def app_auth(consumer_key, consumer_secret):
    app_auth = tweepy.AppAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
    app_api = tweepy.API(app_auth)
    return app_api


class Point:
    """ Geo Point
    """
    
    def __init__(self, latitude: float, longitude: float):
        """ Init Point with lat:float and long:float
        """
        self.latitude = latitude
        self.longitude = longitude
    
    def get_tuple(self):
        # return self.latitude, self.longitude
        return self.longitude, self.latitude


class Tweet():
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
    
    def extract_point(self):
        if self._tweet.coordinates:
            coord = self._tweet.coordinates.get('coordinates', None)
            self._point = Point(float(coord[1]), float(coord[0]))
        return self._point
    
    def get_creation_time(self) -> float:
        """
        Time of post creation
        :return: timestamp
        """
        return time.mktime(self._tweet.created_at.timetuple())
    
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
    
    def for_csv(self):
        return  self._point.get_tuple(), \
                self.get_lang(), \
                self.get_text(), \
                self.get_tags(), \
                self.get_creation_time(), \
                self.get_user_id(), \
                self._tweet


def today():
    return f"{datetime.datetime.today().time().hour}_" \
           f"{datetime.datetime.today().time().minute}__" \
           f"{datetime.datetime.today().date().day}_" \
           f"{datetime.datetime.today().date().month}_" \
           f"{datetime.datetime.today().date().year}"


def get_dest(n_cords):
    if n_cords:
        return "wo_coords"
    else:
        return "with_coords"


def save_to_csv(posts, city, language, without_cords):
    df = pd.DataFrame(columns=['coordinates',
                               'language',
                               'text',
                               'tags',
                               'creation_time',
                               'user_id',
                               'post'])
    
    for i, post in enumerate([Tweet(tweet, cities[city_name]) for tweet in posts]):
        df.loc[i] = post.for_csv()
    
    df.to_csv(f"posts/tweets/{get_dest(without_cords)}/{city}_{language}_{today()}.csv", encoding='utf-8')


# Try to get all


cities = {
    "kzn": Point(55.7714676, 49.0887294),
    "spb": Point(59.9330659, 30.3059148),
    "msk": Point(55.7564364, 37.5446647),
    "soc": Point(43.6025106, 39.7107868),
    "ros": Point(47.2441707, 39.595124),
    "kad": Point(54.7252967, 20.4338166),
    "vod": Point(48.6627428, 44.4551274),
    "sar": Point(51.5572534, 45.9373729),
    "sam": Point(53.2235426, 50.1559591),
    "ekb": Point(56.8501552, 60.5699289),
    "niz": Point(56.2953442, 43.936181)
}

app_api = app_auth(credentials[1]['api_key'], credentials[1]['api_secret'])
app_api.wait_on_rate_limit = True
app_api.wait_on_rate_limit_notify = True

q = '*'

# TODO: get rid of
count = 10

while True:
    
    print("\n\nLet's start new cycle!\n")
    
    for city_name in cities.keys():
        geocode = "%f,%f,%s" % (cities[city_name].latitude, cities[city_name].longitude, '50km')
        
        for lang in ['ru', 'en', 'all_lngs']:
    
            for wo_coords in [False, True]:
    
                print(f"Searching for tweets in {city_name}")
                print(f"Searching for tweets in {lang}")
                print(f"Searching for tweets with coordinates: {not wo_coords}")
    
                tweets = []
                try:
                    if lang != "all_lngs":
                        for t in tweepy.Cursor(app_api.search,
                                               q=q,
                                               geocode=geocode,
                                               lang=lang).items(count):
                            if t.coordinates or wo_coords:
                                tweets.append(t)
                    else:
                        for t in tweepy.Cursor(app_api.search,
                                               q=q,
                                               geocode=geocode).items(count):
                            if t.coordinates or wo_coords:
                                tweets.append(t)
    
                except Exception as e:
                    print(e)
    
                print(f"Found tweets {len(tweets)}\n")
    
                if len(tweets) > 0:
                    save_to_csv(tweets, city_name, lang, wo_coords)
        
    print("\n\n    ATTENTION! \n\nSleeping for a week, see ya!\n")
    # time.sleep(6 * 24 * 60 * 60 * 60)
    time.sleep(60)