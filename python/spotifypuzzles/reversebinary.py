# Vishal Vivek Prasad 2014, Spotify Lab Puzzle # 3
import sys

def bitreverse(n):
    num = list(bin(n)[2:])
    num_len = len(num)
    for i in range(int(num_len / 2)):
        tmp = num[i]
        num[i] = num[num_len - 1 - i]
        num[num_len - 1 - i] = tmp
    print int(''.join(num), 2)

bitreverse(int(sys.argv[1]))
