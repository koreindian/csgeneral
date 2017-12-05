f = open('rosalind_revc.txt', 'r')

cpl = ''

for line in f:
    for c in line.strip()[::-1]:
        if c == 'A':
            cpl += 'T'
        elif c == 'T':
            cpl += 'A'
        elif c == 'C':
            cpl += 'G'
        elif c == 'G':
            cpl += 'C'

print(cpl)    
