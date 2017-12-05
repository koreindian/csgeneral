f = open('rosalind_dna.txt', 'r')

ncount = {'A': 0, 'T': 0, 'C': 0, 'G': 0}

for line in f:
    for c in line.strip():
        ncount[c] += 1

print (ncount['A'], ncount['C'], ncount['G'], ncount['T'])

f.close()
