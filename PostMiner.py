import tweepy
import time
import pandas as pd
import datetime

from Twitter import Twitter
from models.Point import Point


class PostMiner:
    def __init__(self):
        self.networks = {
            'twitter': Twitter()
        }
    
    def get_posts(self, points, networks=None, langs=None, count = -1):
        if not networks:
            networks = self.networks.keys()
        if not langs:
            langs = ['ru', 'en', 'all_lngs']
            
        for net_name in networks:
            
            for point, point_name in zip(points.values(), points.keys()):
                
                for lang in langs:
                    
                    for wo_coords in [False, True]:
                        print("Searching:")
                        print(f"Place:       {point_name}")
                        print(f"Lang:        {lang}")
                        print(f"Coordinates: {not wo_coords}")
                        
                        try:
                            posts = self.networks[net_name].get_posts(point, lang, wo_coords, count)
                            
                            print(f"Found tweets {len(posts)}\n")
                            
                            if len(posts) > 0:
                                self.save_to_csv(net_name, posts, point_name, lang, wo_coords)
                        except Exception as e:
                            print(e)
    
    def get_dest(n_cords):
        if n_cords:
            return "wo_coords"
        else:
            return "with_coords"

    def save_to_csv(self, network, posts, city, language, without_cords):
        df = pd.DataFrame(columns=['coordinates',
                                   'language',
                                   'text',
                                   'tags',
                                   'creation_time',
                                   'user_id',
                                   'models'])
        
        for i, post in enumerate(posts):
            df.loc[i] = post.for_csv()

        df.to_csv(f"posts/{network}/{self.get_dest(without_cords)}/{city}_{language}_{self.today()}.csv", encoding='utf-8')

    def today(self):
        return f"{datetime.datetime.today().time().hour}_" \
               f"{datetime.datetime.today().time().minute}__" \
               f"{datetime.datetime.today().date().day}_" \
               f"{datetime.datetime.today().date().month}_" \
               f"{datetime.datetime.today().date().year}"


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

pm = PostMiner()

while True:
    
    print("\n\nLet's start new cycle!\n")
    
    pm.get_posts(cities)
    
    # sleep_time = 6 * 24 * 60 * 60 * 60
    sleep_time = 60
    
    print(f"\n\n    ATTENTION! \n\nSleeping for {sleep_time} seconds, see ya!\n")
    
    time.sleep(sleep_time)