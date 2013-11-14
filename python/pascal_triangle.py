# A module that calculates factorials, combinations, binomial coefficients, and Pascal Triangles.
# Written for my own amusement, on 11/13/2013. ~~ Vishal Vivek Prasad

import math

def fac(n):
	if n == 0:
		return 1
	else:
		return n * fac(n-1)


def choose(n,k):
	a = fac(n)
	b = fac(k)
	c = fac(n-k)
	return a/(b*c)


def binomial_prob(p, n, s):
	a = 1/(s**n)
	k = 0
	mySum = 0
	limit = math.floor((p - n)/s)
	while k <= limit:
		b = (-1) ** k
		c = choose(n, k)
		d = choose(p - s*k -1, n-1)
		mySum += b * c * d
		k+=1
	return a * mySum


def binomial_coef(n):
	i = 0
	a = []
	while i <= n:
		a.append(int(choose(n, i)))
		i+=1
	return a

def pascal(n):
	i = 0
	a = []
	while i<=n:
		a.append(binomial_coef(i))
		i+=1
	return a

def pascal_print(n):
	a = pascal(n)
	b = ""
	for row in a:
		for num in row:
			b += str(num) + " "
		print(b)
		b = ""

		
