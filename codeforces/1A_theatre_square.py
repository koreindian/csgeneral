import fileinput

def num_tiles(n, a):
    if (n % a == 0):
        return n / a
    else:
        return n / a + 1

l = fileinput.input()

args = l[0]
info = args.split()

n, m, a = int(info[0]), int(info[1]), int(info[2])

tiles_n = num_tiles(n, a)
tiles_m = num_tiles(m, a)

#print n, m, a, tiles_n, tiles_m
print tiles_n * tiles_m
