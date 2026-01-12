import random
import math

def extended_gcd(a, b):
    """
    Extended Euclidean Algorithm.
    Finds gcd(a, b) and the coefficients x, y such that:
        ax + by = gcd(a, b)
    """
    if b == 0:
        return a, 1, 0

    gcd, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return gcd, x, y


def modular_inverse(a, m):
    """
    Finds the modular inverse of a modulo m.
    This value is needed to compute the RSA private key.
    """
    gcd, x, _ = extended_gcd(a, m)
    if gcd != 1:
        raise ValueError("Modular inverse does not exist.")
    return x % m

# PRIME NUMBER GENERATION (MILLER–RABIN)

def is_probable_prime(number, rounds=8):
    """
    Checks if a number is probably prime
    """
    if number < 2:
        return False

    # Quick checks for small prime divisors
    small_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
    for prime in small_primes:
        if number == prime:
            return True
        if number % prime == 0:
            return False

    # Write number-1 as d * 2^r
    r = 0
    d = number - 1
    while d % 2 == 0:
        d //= 2
        r += 1

    # Perform Miller–Rabin rounds
    for _ in range(rounds):
        a = random.randrange(2, number - 1)
        x = pow(a, d, number)

        if x == 1 or x == number - 1:
            continue

        for __ in range(r - 1):
            x = pow(x, 2, number)
            if x == number - 1:
                break
        else:
            return False

    return True


def generate_random_prime(bits=16):
    """
    Generates a random prime number with the given number of bits.

    """
    if bits < 8:
        raise ValueError("Bit size must be at least 8.")

    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << (bits - 1)) | 1  # ensure correct size and odd
        if is_probable_prime(candidate):
            return candidate


# RSA KEY GENERATION


def generate_rsa_keys(bits=16):
    """
    Generates RSA public and private keys.

    """
    p = generate_random_prime(bits)
    q = generate_random_prime(bits)

    while q == p:
        q = generate_random_prime(bits)

    n = p * q
    phi = (p - 1) * (q - 1)

    # Common RSA public exponent
    e = 65537
    if math.gcd(e, phi) != 1:
        e = 3
        while math.gcd(e, phi) != 1:
            e += 2

    d = modular_inverse(e, phi)

    return (e, n), (d, n)



# KEY VALIDATION


def validate_public_key(public_key):
    """
    Checks whether a public key is valid for RSA encryption.
    """
    e, n = public_key
    if n <= 255:
        raise ValueError("RSA modulus n is too small.")
    if e <= 1:
        raise ValueError("Public exponent must be greater than 1.")
    return True


def validate_private_key(private_key):
    """
    Checks whether a private key is valid for RSA decryption.
    """
    d, n = private_key
    if n <= 255:
        raise ValueError("RSA modulus n is too small.")
    if d <= 1:
        raise ValueError("Private exponent must be greater than 1.")
    return True

# RSA ENCRYPTION / DECRYPTION

def rsa_encrypt_message(message, public_key):
    """
    Encrypts a text message using RSA and a public key.
    Each character is encrypted individually for simplicity.
    """
    validate_public_key(public_key)
    e, n = public_key

    if message is None:
        raise ValueError("Message cannot be None.")

    byte_data = message.encode("utf-8")
    encrypted = [pow(byte, e, n) for byte in byte_data]
    return encrypted


def rsa_decrypt_message(cipher_list, private_key):
    """
    Decrypts a list of encrypted numbers back into the original text
    using the RSA private key.
    """
    validate_private_key(private_key)
    d, n = private_key

    if cipher_list is None:
        raise ValueError("Cipher data cannot be None.")

    decrypted_bytes = bytes([pow(int(c), d, n) for c in cipher_list])
    return decrypted_bytes.decode("utf-8")