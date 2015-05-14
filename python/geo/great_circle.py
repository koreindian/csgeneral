import math

r_earth_miles = 3963.1676
r_earth_kilometers = 6378.1

def main():
    l1 = (41.789687, -87.598201)
    l2 = (41.8789219, -87.6217188)

    d = Distance(l1,l2)
    miles = d.calc_great_circle_distance(True)
    kilometers = d.calc_great_circle_distance(False)
    #d = great_circle_distance(l1, l2)
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

        print "lambda1: ", lambda_1, " lambda2: ", lambda_2
        d_lambda = math.fabs(lambda_1 - lambda_2)
    
        print phi_1, phi_2, d_lambda
        m = math.sin(phi_1) * math.sin(phi_2) + math.cos(phi_1) * math.cos(phi_2) * math.cos(d_lambda)
        print m
        d_sigma = math.acos(m)

        return  r * d_sigma
    
def great_circle_distance(l1, l2):
    

    phi_1 = math.radians(l1[0])
    lambda_1 = math.radians(l1[1])
    phi_2 = math.radians(l2[0])
    lambda_2 = math.radians(l2[1])

    print "lambda1: ", lambda_1, " lambda2: ", lambda_2
    d_lambda = math.fabs(lambda_1 - lambda_2)
    
    print phi_1, phi_2, d_lambda
    m = math.sin(phi_1) * math.sin(phi_2) + math.cos(phi_1) * math.cos(phi_2) * math.cos(d_lambda)
    print m
    d_sigma = math.acos(m)

    d = r_earth_miles * d_sigma
    
    return d
    
if __name__ == "__main__":
    main()
