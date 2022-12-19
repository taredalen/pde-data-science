from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="pde-data-science")

location = geolocator.geocode(f"11 rue blanche, Paris, France")

print(location.raw)