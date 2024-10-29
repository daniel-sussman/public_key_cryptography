from sympy import primerange
from random import sample, choice
from math import gcd
from gmpy2 import powmod

class TrapdoorCipher:
    def __init__(self):
        number_range = (11, 40)
        self.p, self.q = sample(list(primerange(*number_range)), 2)

    def generate_public_key(self):
        p = self.p
        q = self.q
        print("Select two prime numbers and keep them a secret. Here, we've selected:")
        print(f"p = {p}")
        print(f"q = {q}")
        print("\nThe modulus of the arithmetic that will be used is given by their product:")
        print("modulus = p * q")
        modulus = p * q
        print(f"modulus = {p} * {q} = {p * q}")
        print("\nFirst, using the two prime numbers, calculate Euler's totient function: f(n)  = (p-1) x (q-1)")
        print("(that's the number of positive integers that are less than n and coprime to n)\n")
        totient = (p - 1) * (q - 1)
        print(f"totient = ({p} - 1) * ({q} - 1) = {totient}")
        print("\nThen, select ANY totative to f(n).\n")
        print(f"The numbers relatively prime to {totient} and less than it are:")
        options = self.relatively_prime_and_less_than(totient)
        print(options)
        encryption_exponent = choice(options)
        print(f"\nWe'll select {encryption_exponent}.\n")

        self.public_key = (encryption_exponent, modulus)
        print(f"So our public key is (encryption_exponent, modulus), or {self.public_key}")
        print("(in practice the numbers would be very much larger)")
        
        return self.public_key
    
    def generate_private_key(self):
        encrypt_exponent, modulus = self.public_key
        totient = (self.p - 1) * (self.q - 1)
        decrypt_exponent = self.mod_inverse(encrypt_exponent, totient)

        print("private decrypt exponent = the modular multiplicative inverse of the public encryption_exponent and f(n)\n")
        print(f"public decrypt exponent = {encrypt_exponent} , and f(n) = {totient}")
        print(f"(private decrypt exponent * {encrypt_exponent}) % {totient} = 1")
        print(f"private decrypt exponent = {decrypt_exponent}")
        print(f"\n(this is because {decrypt_exponent} * {encrypt_exponent} = {decrypt_exponent * encrypt_exponent}, which is 1 more than {decrypt_exponent * encrypt_exponent - 1}, which is a factor of {totient}.)")

        self.private_key = (decrypt_exponent, modulus)
        print(f"\nSo our private key is (decryption_exponent, modulus), or {int(self.private_key[0]), self.private_key[1]}")
        
        return self.private_key

    def relatively_prime_and_less_than(self, number):
        return [n for n in range(2, number + 1) if gcd(n, number) == 1]

    def mod_inverse(self, a, n):
        return powmod(a, -1, n)

def encrypt(message, public_key):
    encrypt_exponent, modulus = public_key

    print(f"message = {message}")
    print("encrypted_message = (message ** public encrypt exponent) % n")
    print(f"public encrypt exponent = {encrypt_exponent}, and modulus = {modulus}")
    print(f"encrypted_message = ({message} ** {encrypt_exponent}) % {modulus}")
    
    encrypted_message = (message ** encrypt_exponent) % modulus
    print(f"encrypted_message = {encrypted_message}")
    return encrypted_message

def decrypt(encrypted_message, private_key):
    decrypt_exponent, modulus = private_key

    print(f"The encrypted message is: {encrypted_message}.\n")
    print("decrypted_message = (encrypted_message ** private decrypt exponent) % n")
    print(f"private decrypt exponent = {decrypt_exponent}, and modulus = {modulus}")
    print(f"decrypted_message = ({encrypted_message} ** {decrypt_exponent}) % {modulus}")
    print(f"decrypted_message = ({encrypted_message ** decrypt_exponent}) % {modulus}")

    decrypted_message = (encrypted_message ** decrypt_exponent) % modulus
    print(f"decrypted_message = {decrypted_message}")
    return decrypted_message

# Euler's Totient function, ϕ(n), is the number of positive integers that are less than n and coprime to n. 