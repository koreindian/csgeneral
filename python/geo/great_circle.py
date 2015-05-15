'''
Program: great_circle.py
By: Vishal Prasad, 2015

Calculates the distance between two location, given their addresses.
Uses Nominatim to resolve address queries.
 Warning: Nominatim requests may timeout.

Uses great circle distance.
'''

import math
from geopy.geocoders import Nominatim

r_earth_miles = 3963.1676
r_earth_kilometers = 6378.1

def main():
    print "great_circle.py"
    print "Calculate the distance between any two addresses!"
    print "Using great circle distance,"

    geolocator = Nominatim()

    address1 = input('Enter address 1 (Use quotation marks): ')
    location1 = geolocator.geocode(address1, timeout=10)
    print location1.address

    address2 = input('Enter address 2 (Use quotation marks): ')
    location2 = geolocator.geocode(address2, timeout=10)    
    print location2.address

    l1 = (location1.latitude, location1.longitude)
    l2 = (location2.latitude, location2.longitude)
    

    d = Distance(l1,l2)
    miles = d.calc_great_circle_distance(True)
    kilometers = d.calc_great_circle_distance(False)
    print "Distance (mi): ", miles
    print "Distance (km): ", kilometers

class Distance:
    def __init__ (self, location_1, location_2):
        self.l1 = location_1
        self.l2 = location_2

    def calc_great_circle_distance (self, in_miles):
        if in_miles:
            r = r_earth_miles
        else:
            r = r_earth_kilometers

        phi_1 = math.radians(self.l1[0])
        lambda_1 = math.radians(self.l1[1])
        phi_2 = math.radians(self.l2[0])
        lambda_2 = math.radians(self.l2[1])

        d_lambda = math.fabs(lambda_1 - lambda_2)
    
        m = math.sin(phi_1) * math.sin(phi_2) + math.cos(phi_1) * math.cos(phi_2) * math.cos(d_lambda)
        d_sigma = math.acos(m)

        return  r * d_sigma

    
if __name__ == "__main__":
    main()
