import fileinput

def abv_word(word):
    l = len(word)
    if l <= 10:
        return word

    return word[0] + str(l - 2) + word[l-1]

l = fileinput.input()

n = int(l[0])

for line in l:
    word = line.strip()
    print abv_word(word)



