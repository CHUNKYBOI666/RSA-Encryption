import random
from math import gcd

class RSAKeyPair:
    def __init__(self):
        self.public_key = None
        self.private_key = None

    def is_prime(self, n):
        if n <= 1:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True

    def next_prime(self, n):
        while True:
            n += 1
            if self.is_prime(n):
                return n

    def mod_inverse(self, e, phi):
        def egcd(a, b):
            if b == 0:
                return a, 1, 0
            g, y, x = egcd(b, a % b)
            return g, x, y - (a // b) * x

        g, x, y = egcd(e, phi)
        if g != 1:
            raise Exception("Modular inverse doesn't exist")
        return x % phi

    def generate_keys(self):
        p = self.next_prime(random.randint(100, 300))
        q = self.next_prime(random.randint(300, 600))
        n = p * q
        phi = (p - 1) * (q - 1)

        e = 3
        while gcd(e, phi) != 1:
            e += 2

        d = self.mod_inverse(e, phi)

        self.public_key = (e, n)
        self.private_key = (d, n)

        return self.public_key, self.private_key
