import fileinput

l = fileinput.input()

args = l[0]
info = args.split()
w = int(info[0])

if ((w % 2 == 0) and (w != 2)):
    print "YES"
else:
    print "NO"
