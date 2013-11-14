# A little module that generates random times.
# Written to facilitate Japanese study, on 11/13/2013. ~~ Vishal Vivek Prasad

import random

def random_time(n):
	while n>0:
		hour = random.randrange(1, 12)
		minute = random. randrange(0, 59)
		print ('Time: %(h)02d:%(m)02d' % {"h": hour, "m":minute})
		n -= 1

