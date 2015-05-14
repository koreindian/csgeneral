#Just a caeser cipher

def main():
    message  = input("Enter message: ")
    key = 13
    ciphertext = encrypt(message, key)
    print "ciphertext: ", ciphertext

    plaintext = decrypt(ciphertext, key)
    print "plaintext: ", plaintext

    brute_force_decrypt(ciphertext)
def encrypt(m, k):
    m = m.upper()
    cipher = ''

    for char in m:
        if char == ' ':
            cipher += char
        else:
            cipher +=  chr((ord(char) - 65 + k) % 26 + 65)
    
    return cipher

def decrypt(m, k):
    plaintext = ''

    for char in m:
        if char == ' ':
            plaintext += char
        else:
            plaintext += chr((ord(char) - 65 - k) % 26 + 65)

    return plaintext

def brute_force_decrypt(m):
    for i in range(26):
        print "key: ", i, "\t message: ", decrypt(m,i)

if __name__ == "__main__":
    main()
