import numpy
import random

def primesfrom2to(n):
    """ Input n>=6, Returns a array of primes, 2 <= p < n """
    sieve = numpy.ones(n/3 + (n%6==2), dtype=numpy.bool)
    for i in xrange(1,int(n**0.5)/3+1):
        if sieve[i]:
            k=3*i+1|1
            sieve[       k*k/3     ::2*k] = False
            sieve[k*(k-2*(i&1)+4)/3::2*k] = False
    return numpy.r_[2,3,((3*numpy.nonzero(sieve)[0][1:]+1)|1)]

def get_coprime(z, primes):
    p = 0
    remainder = 0
    while (remainder == 0 and p < z):
        p = random.choice(primes)
        remainder = z % p
    return p

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def expmod(a,b,c):
	x = 1
	while(b>0):
		if(b&1==1): x = (x*a)%c
		a=(a*a)%c
		b >>= 1
	return x%c

def generateKeyPair():
    primes = primesfrom2to(2**16-1)

    (p, q) = random.sample(primes, 2)
    n = long(p)*long(q)
    z = long(p-1)*long(q-1)
    k = long(get_coprime(z, primes))

    (_, j1, j2) = egcd(k, z)
    if j1 > 0:
        j = j1
    else:
        j = j2

    print('should be 1: ' + str((long(k) * long(j)) % long(z)))

    print('n = ' + str(n))
    print('j = ' + str(j))
    print('k = ' + str(k))

    plaintext = long(14)
    encrypted = expmod(plaintext, k, n)
    decrypted = expmod(encrypted, j, n)
    print('should be 14: ' + str(decrypted))

    encrypted = expmod(plaintext, j, n)
    decrypted = expmod(encrypted, k, n)
    print('should be 14: ' + str(decrypted))

def decrypt(message, publicKey, sharedModulus):
    return expmod(message, publicKey, sharedModulus)

generateKeyPair()
