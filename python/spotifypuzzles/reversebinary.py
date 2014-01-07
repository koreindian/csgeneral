import math
import string

def bitreverse(n):
    num = list(bin(n)[2:])
    num_len = len(num) - 1
    for i in range(int(num / 2)):
        tmp = num[i]
        num[i] = num[num_len - i]
        num[num_len - i] = tmp
    print (num)
        
x = int(input('Enter an integer between 1 and 1,000,000,000\n>'))
bitreverse(x)
