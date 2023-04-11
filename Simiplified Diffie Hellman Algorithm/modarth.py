from math import sqrt, prod

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

def power(x: int, y: int, p: int) -> int:
  res = 1
  x = x % p
  while (y > 0):
    if (y & 1):
      res = (res * x) % p
    y = y >> 1
    x = (x * x) % p
  return res

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

def findPrimitive(n: int) -> set:
  primitives = set()
  if (not(isPrime(n))):
    return primitives
  totient = n - 1
  s = findPrimeFactors(totient)
  for r in range(2, totient + 1):
    flag = False
    for it in s:
      if (power(r, totient // it, n) == 1):
        flag = True
        break
    if (flag == False):
      primitives.add(r)
  return primitives

def eulerTotient(num: int) -> int:
  if(isPrime(num)):
    return (num - 1)
  else:
    return prod([i - 1 for i in findPrimeFactors(num)])

def isPrimitive(of: int, num: int, all=False) -> bool:
  if((of == 2 and num == 1) or (of == 1 and num == 0)):
    return True
  if((num == 0) or (not(all or isPrime(of))) or (of == 1 and num == 1)):
    return False
  s = set()
  totient = eulerTotient(of)
  s = findPrimeFactors(totient)
  for it in s:
    if (power(num, totient // it, of) == 1):
      return False
  return True
