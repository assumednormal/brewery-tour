"""
In the original post, FlowingData used the Google Maps API to get travel distances and times between each pair of
breweries. Unfortunately the Google Maps API charges $0.005 per pair. With the initial address sanitization we went from
8,993 breweries down to 7,455. That translates to 27,784,785 pairs of breweries and $138,923.93 in charges.

If actual driving distances aren't easy or cheap to obtain, we can first try calculating distances between pairs of
breweries by geocoding each brewery's address and then using Vincenty distance[1] to calculate the distance.

[1] https://en.wikipedia.org/wiki/Vincenty%27s_formulae
"""

import json
import re
from tqdm import tqdm

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

with open("us-breweries-with-valid-addresses.json", "r") as f:
    breweries = json.load(f)

geolocator = Nominatim(user_agent="brewery_tour")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1)

def geolocate(brewery):
    # plus-four codes don't seem to be handled well, so remove them here
    address = brewery["address"]
    address = re.sub(r"\-\d{4}", "", address)
    location = geocode(address)
    if location and location.latitude and location.longitude:
        brewery["coordinates"] = (location.latitude, location.longitude)      
    return brewery

with_coordinates = map(geolocate, breweries)
has_coordinates = filter(lambda brewery: "coordinates" in brewery, tqdm(with_coordinates))

with open("us-breweries-with-coordinates.json", "w") as f:
    json.dump(list(has_coordinates), f)