#Just a simple reverse cipher


def main():
    message = input('Enter message: ')
    ciphertext = encrypt(message)

    print ciphertext
    
    plaintext = decrypt(ciphertext)
    
    print plaintext

def encrypt(m):
    n = ''
    
    i = len(m) - 1
    while i >= 0:
        n = n + m[i]
        i -= 1

    return n

def decrypt(m):
    return encrypt(m)


if __name__ == "__main__":
    main()
