import fileinput

l = fileinput.input()

args = l[0]
info = args.split()
n = int(info[0])
k = int(info[1])

args = l[1]
info = args.split()

count = 0
if int(info[k-1]) == 0:
    for i in range(k):
        if int(info[i]) > 0:
            count += 1

else:
    count = k
    for i in range(k, n):
        if int(info[i]) == int(info[k-1]):
            count += 1
            #print "Hi"
        else:
            break
        
print count
