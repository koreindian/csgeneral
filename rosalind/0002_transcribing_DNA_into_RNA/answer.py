f = open('rosalind_rna.txt', 'r')

for line in f:
    print(line.replace('T', 'U'))

f.close()

