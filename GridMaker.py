import json
import pylab as pl
from math import radians, cos, sin, asin, sqrt
from models.Point import Point


def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371 * c
    return km


def mk_grid(center: Point, R, r=20):
    step = r * 1 / 2
    # the number of kilometers in one radian
    # kms_per_radian = 6371.0088
    # radian_per_km = 0.00015696101377226163
    deg_per_km = 0.0089932036372453797
    
    R_rad = deg_per_km * R
    r_rad = deg_per_km * r
    step_rad = deg_per_km * step
    lat_range = [i for i in pl.frange(center.latitude - R_rad + r_rad, center.latitude + R_rad - r_rad, step_rad)]
    lng_range = [i for i in
                 pl.frange(center.longitude - (deg_per_km * R), center.longitude + (deg_per_km * R), step_rad)]
    grid = []
    for x in lat_range:
        for y in lng_range:
            grid.append(Point(x, y))
    return grid


def grid_to_geojson(grid, save_to='', name='test'):
    features = [{
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [point.longitude, point.latitude]
        },
        "properties": {
            "title": '',
            "marker-symbol": "monument"
        }} for point in grid]
    geo_j = {
        "type": "FeatureCollection",
        "features": features
    }
    with open(save_to + '/' + name + '.geojson', 'w') as output:
        json.dump(geo_j, output)
    return grid


def get_geoj_grid(center, R, r, save_to='', name='test'):
    return grid_to_geojson(mk_grid(center, R, r), save_to, name)
