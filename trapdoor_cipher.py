from sympy import primerange
from random import sample, choice
from math import gcd
from gmpy2 import powmod

class TrapdoorCipher:
    def __init__(self):
        number_range = (11, 40)
        self.p, self.q = sample(list(primerange(*number_range)), 2) # select two primes within number_range

    def generate_public_key(self, print_stuff=True):
        p = self.p
        q = self.q
        modulus = p * q
        totient = (p - 1) * (q - 1)
        options = self.relatively_prime_and_less_than(totient)
        encryption_exponent = choice(options)
        self.public_key = (encryption_exponent, modulus)
        
        if print_stuff:
            print(
                "\n" \
                "Select two prime numbers and keep them a secret. Here, we've selected:\n" \
                f"  p = {p}\n" \
                f"  q = {q}\n\n" \
                "The modulus N is given by their product:\n" \
                "  N = p * q\n" \
                f"  N = {p} * {q} = {p * q}\n\n" \
                "First, using the two prime numbers, calculate Euler's totient function φ(N)\n" \
                "(that's the number of positive integers that are less than and coprime to N).\n\n" \
                "The totient function is multiplicative, so φ(p * q) = φ(p) * φ(q)\n"
                "and the totient of any prime number n is n - 1.\n\n"
                "  φ(N) = (p - 1) * (q - 1)\n"
                f"  φ({modulus}) = ({p} - 1) * ({q} - 1) = {totient}\n\n" \
                "Now we select the public exponent e, which can be ANY number such that 1 < e < φ(N)\n"
                "and e is coprime to φ(N).\n\n" \
                f"The numbers coprime to {totient} and less than it are:\n" \
                f"{options}\n\n" \
                f"We'll select {encryption_exponent}.\n\n" \
                f"So our public key is (e, N), or {self.public_key}\n" \
                "(in practice the numbers would be very much larger)\n"
            )

        return self.public_key
    
    def generate_private_key(self, print_stuff=True):
        encrypt_exponent, modulus = self.public_key
        totient = (self.p - 1) * (self.q - 1)
        decrypt_exponent = self.mod_inverse(encrypt_exponent, totient)
        self.private_key = (decrypt_exponent, modulus)

        if print_stuff:
            print(
                "\n" \
                "d = the modular multiplicative inverse of e and φ(N)\n" \
                "(that is, we need to find d such that (d * e) mod φ(N) = 1)\n\n"
                f"e = {encrypt_exponent}, and φ(N) = {totient}\n\n" \
                f"So using the extended Euclidean algorithm, we compute:\n" \
                f"  d = {decrypt_exponent}\n\n" \
                f"(We can confirm that {decrypt_exponent} * {encrypt_exponent} = {decrypt_exponent * encrypt_exponent}, and {decrypt_exponent * encrypt_exponent} % {totient} = 1.)\n\n" \
                f"So our private key is (d, N), or {int(self.private_key[0]), self.private_key[1]}\n" \
            )
        return self.private_key

    def relatively_prime_and_less_than(self, number):
        return [n for n in range(2, number) if gcd(n, number) == 1]

    def mod_inverse(self, a, n):
        return powmod(a, -1, n)

def encrypt(message, public_key, print_stuff=True):
    encrypt_exponent, modulus = public_key
    encrypted_message = (message ** encrypt_exponent) % modulus

    if print_stuff:
        print(
            f"message = {message}\n" \
            "encrypted_message = (message ^ e) mod N\n\n" \
            "from the public key, we have:\n" \
            f"  e = {encrypt_exponent}, and N = {modulus}\n\n" \
            f"so, encrypted_message = ({message} ** {encrypt_exponent}) % {modulus} = {encrypted_message}\n"
        )

    return encrypted_message

def decrypt(encrypted_message, private_key, print_stuff=True):
    decrypt_exponent, modulus = private_key
    decrypted_message = (encrypted_message ** decrypt_exponent) % modulus

    if print_stuff:
        print(
            f"The encrypted message is: {encrypted_message}.\n\n" \
            "decrypted message = (encrypted message ^ d) mod N\n\n" \
            f"from our private key, d = {decrypt_exponent} and N = {modulus}\n" \
            f"decrypted message = ({encrypted_message} ** {decrypt_exponent}) % {modulus}\n"
            f"decrypted message = ({encrypted_message ** decrypt_exponent}) % {modulus}\n\n"
            f"decrypted message = {decrypted_message}"
        )

    return int(decrypted_message)

def encrypt_message(message, public_key):
    plaintext = [ord(char) for char in message]
    ciphertext = [encrypt(char, public_key, print_stuff=False) for char in plaintext]
    result = stringify(ciphertext)
    print(
        "\n" \
        f"  1) Get the ascii value of each character:\n" \
        f"{plaintext}\n\n" \
        f"  2) Encrypt each value:\n" \
        f"{ciphertext}\n\n" \
        "  3) Output the result to a single string.\n"
    )

    return result

def decrypt_message(encrypted_message, private_key):
    ciphertext = destringify(encrypted_message)
    plaintext = [decrypt(char, private_key, print_stuff=False) for char in ciphertext]
    result = ''.join(chr(num) for num in plaintext)
    print(
        "\n" \
        f"  1) Decompose the string into a list of values:\n" \
        f"{ciphertext}\n\n" \
        f"  2) Decrypt each value:\n" \
        f"{plaintext}\n\n" \
        "  3) Convert ascii values back to characters.\n"
    )

    return result

def stringify(message_string):
    string_values = [f"{num:03d}" for num in message_string]
    return ''.join(string_values)

def destringify(message_string, increment=3):
    return [int(message_string[i : i + increment]) for i in range(0, len(message_string), increment)]

# Euler's Totient function, ϕ(N), is the number of positive integers that are less than n and coprime to n. 