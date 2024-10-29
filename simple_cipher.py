ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

class Cipher:
    def __init__(self, key):
        self.key = key
        self.cipher = self.build_cipher(key)

    def encrypt(self, message):
        encrypted_message = ""

        for char in message:
            if char.isalpha():
                index = ALPHABET.index(char.upper())
                encrypted_message += self.cipher[index]
            else:
                encrypted_message += char
        
        return encrypted_message

    def decrypt(self, encrypted_message):
        decrypted_message = ""

        for char in encrypted_message:
            if char.isalpha():
                index = self.cipher.index(char.upper())
                decrypted_message += ALPHABET[index]
            else:
                decrypted_message += char
        
        return decrypted_message


    def build_cipher(self, key):
        cipher_alphabet = self.list_unique_letters(key) # begin with unique letters in the key
        for letter in ALPHABET:
            if not letter in cipher_alphabet:
                cipher_alphabet.append(letter) # add the rest of the letters in alphabetical order
        
        return cipher_alphabet
    
    def list_unique_letters(self, key):
        # list all unique letters in key, in order
        result = []

        for char in key:
            if not char.isalpha():
                continue # skip characters that aren't letters

            letter = char.upper() # make all letters uppercase
            if not letter in result:
                result.append(letter) # add the letter to result if not already there

        return result