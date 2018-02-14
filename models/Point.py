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