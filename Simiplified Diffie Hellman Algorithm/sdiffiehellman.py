from modarth import isPrimitive, isPrime

def publicKey(privateKey: int, prime: int, generator: int) -> int:
  return (generator ** privateKey) % prime

def secret(private: int, public: int, prime: int) -> int:
  return (public ** private) % prime

def main():
  p = int(input('Enter the prime number: '))
  while(not(isPrime(p))):
    p = int(input(f'Number {p} is not prime\nEnter the prime number: '))

  g = int(input('Enter the generator number: '))
  while(not(isPrimitive(p, g))):
    g = int(input(f'Number {g} is not generator of {p}\nEnter the generator number: '))

  KRA = int(input('Enter the private key for USER A: '))
  KUA = publicKey(KRA, p, g)
  print(f'Public key of USER A is: {KUA}')

  KRB = int(input('Enter the private key for USER B: '))
  KUB = publicKey(KRB, p, g)
  print(f'Public key of USER B is: {KUB}')

  print('After exchanging public keys,')

  SA = secret(KRA, KUB, p)
  SB = secret(KRB, KUA, p)

  print(f'Shared secret computed on USER A\'s side is {SA}')
  print(f'Shared secret computed on USER B\'s side is {SB}')

  if(SA == SB):
    print('Correct Key exchanged')
  else:
    print('Some computational Error')

if __name__ == '__main__':
  main()