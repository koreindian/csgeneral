#Just a caeser cipher

def main():
    message  = "Attack at dawn       "
    key = 1
    ciphertext = encrypt(message, key)
    print ciphertext

    plaintext = decrypt(ciphertext, key)
    print plaintext

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

if __name__ == "__main__":
    main()
