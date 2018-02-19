import tweepy

from models.post.Tweet import Tweet
from providers.PostProvider import PostProvider


class Twitter(PostProvider):
    
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

    def __init__(self):
        cred = self.credentials[0]
        self.app_auth(cred['api_key'], cred['api_secret'])
        
    def app_auth(self, consumer_key, consumer_secret):
        app_auth = tweepy.AppAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret)
        self.app_api = tweepy.API(app_auth)
        self.app_api.wait_on_rate_limit = True
        self.app_api.wait_on_rate_limit_notify = True
    
    def get_posts(self, point, radius=50, lang='en', wo_coords=False, count=0):
        q = '*'
        geocode = f"{point.latitude},{point.longitude},{radius}km"
        
        tweets = []
        try:
            if count > 0:
                if lang != "all_lngs":
                    for t in tweepy.Cursor(self.app_api.search,
                                           q=q,
                                           geocode=geocode,
                                           lang=lang).items(count):
                        if t.coordinates or wo_coords:
                            tweets.append(t)
                else:
                    for t in tweepy.Cursor(self.app_api.search,
                                           q=q,
                                           geocode=geocode).items(count):
                        if t.coordinates or wo_coords:
                            tweets.append(t)
            else:
                if lang != "all_lngs":
                    for t in tweepy.Cursor(self.app_api.search,
                                           q=q,
                                           geocode=geocode,
                                           lang=lang).items():
                        if t.coordinates or wo_coords:
                            tweets.append(t)
                else:
                    for t in tweepy.Cursor(self.app_api.search,
                                           q=q,
                                           geocode=geocode).items():
                        if t.coordinates or wo_coords:
                            tweets.append(t)
        except Exception as e:
            print(e)
        return [Tweet(tweet, point) for tweet in tweets]
