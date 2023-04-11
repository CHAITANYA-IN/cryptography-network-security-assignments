from math import sqrt, prod

def gcdExtended(a: int, b: int) -> tuple[int, int, int]:
    if(a == 0):
      return b, 0, 1
    gcd, x1, y1 = gcdExtended(b%a, a) 
    x = y1 - (b//a) * x1 
    y = x1
    return (gcd, x, y)

def isPrime(num: int) -> bool:
  if(num < 2):
    return False
  prime = [True for i in range(num+1)]
  p = 2
  while (p * p <= num):
    if (prime[p] == True):
      for i in range(p * p, num+1, p):
        prime[i] = False
    p += 1
  return prime[num]

def findPrimeFactors(n: int) -> set:
  s = set()
  while (n % 2 == 0):
    s.add(2)
    n = n // 2
  for i in range(3, int(sqrt(n)), 2):
    while (n % i == 0):
      s.add(i)
      n = n // i
  if (n > 2):
    s.add(n)
  return s

def eulerTotient(num: int) -> int:
  if(isPrime(num)):
    return (num - 1)
  else:
    return prod([i - 1 for i in findPrimeFactors(num)])

def isCoprime(n1: int, n2: int) -> bool:
  return (gcdExtended(n1, n2)[0] == 1)

def modInverse(inv: int, mod: int) -> int or None:
  gcd, x, y = gcdExtended(inv, mod)
  if(gcd == 1):
    return ((x % mod) + mod) % mod

def getCoprimesFor(num: int) -> list:
  return [i for i in range(num) if isCoprime(i, num)]