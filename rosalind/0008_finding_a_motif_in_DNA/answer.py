def main():
    print(substring('GATATATGCATATACTT', 'ATAT'))
    
    test1 = read_input()
    print(substring(test1[0], test1[1]))

def substring(s, t):
    print(s)
    print(t)
    indexes = ''
    for i in range(len(s) - len(t) + 1):
        if t == s[i:i+len(t)]:
            indexes += str(i+1) + ' '
    return indexes

def read_input():
    f = open('rosalind_subs.txt', 'r')
    s = f.readline().strip()
    t = f.readline().strip()
    f.close()
    return s, t

if __name__ == '__main__':
    main()
