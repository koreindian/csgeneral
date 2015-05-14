import math

def main():
    message = "Common sense is not so common."
    key = 8

    ciphertext = encrypt(message, key)
    print ciphertext
    plaintext = decrypt(ciphertext, key)
    print plaintext

def encrypt(m, k):
    ciphertext = ''
    for i in range(k):
        j = i
        while j < len(m):
            ciphertext += m[j]
            j += k

    return ciphertext

def decrypt(m, k):
    k2 = int( math.ceil( float(len(m)) / k))
    print k2
    plaintext = encrypt(m, k2)
    return plaintext

if __name__ == "__main__":
    main()
