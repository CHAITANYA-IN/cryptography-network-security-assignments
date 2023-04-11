from random import randint
from modarth import isPrime, eulerTotient, getCoprimesFor, modInverse

def operation(text, key):
  return (text ** key[0]) % key[1]

def encrypt(plainText: int, publicKey: tuple[int, int]):
  return operation(plainText, publicKey)

def decrypt(cipherText: int, privateKey: tuple[int, int]):
  return operation(cipherText, privateKey)


p = int(input('Enter the prime number: '))
while(not(isPrime(p))):
  p = int(input(f'Number {p} is not prime\nEnter the prime number: '))

q = int(input('Enter the prime number: '))
while(not(isPrime(q))):
  q = int(input(f'Number {q} is not prime\nEnter the prime number: '))

n = p * q
m = eulerTotient(p) * eulerTotient(q)
coprimes = getCoprimesFor(m)
try:
  coprimes.remove(1)
except ValueError:
  pass
e = coprimes[randint(0, len(coprimes))]
d = modInverse(e, m)

KR = (d, n)
KU = (e, n)

print(f'Private Key = {KR}')
print(f'Public Key = {KU}')

x = int(input('Enter a number as plain text: '))

y = encrypt(x, KU)
print('Cipher Text is:', y)

num = decrypt(y, KR)
print('Deciphered Text is:', num)