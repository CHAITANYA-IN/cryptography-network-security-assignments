def encrypt(key, text):
  import numpy as np, re
  K_vector = np.array([26 if i == '.' else 27 if i == ',' else 28 if i == '!' else ord(i) - ord('a') for i in re.sub(r'[^\.\!\,a-zA-Z]+', '', key.lower())])
  K = K_vector.reshape(3, 3)
  if (np.linalg.det(K) == 0):
    print("ValueError: Key forms singular matrix")
    exit()
  l = [ord(i) - ord('a') for i in re.sub(r'[^\.\!\,a-zA-Z]+', '', text.lower())]
  P = np.array([26 if x == -51 else 27 if x == -53 else 28 if x == -64 else x for x in l] + [23] * ((3 - len(l) % 3) % 3)).reshape(-1, 3).T
  return (''.join(['.' if i == 26 else ',' if i == 27 else '!' if i == 28 else chr(i + ord('a')) for i in (K.dot(P) % 29).T.reshape(-1)]), len(l))


def decrypt(key, cipher):
  import numpy as np, sympy as sp, re
  try:
    K_vector = np.array([26 if i == '.' else 27 if i == ',' else 28 if i == '!' else ord(i) - ord('a') for i in re.sub(r'[^\.\!\,a-zA-Z]+', '', key.lower())])
    K_inv = np.array(sp.Matrix(K_vector.reshape(3, 3)).inv_mod(29))
  except ValueError:
    print("ValueError: Key forms singular matrix")
    exit()
  l = [ord(i) - ord('a') for i in re.sub(r'[^\.\!\,\#a-zA-Z]+', '', cipher.lower())]
  C = np.array([26 if x == -51 else 27 if x == -53 else 28 if x == -64 else x for x in l]).reshape(-1, 3).T
  return ''.join(['.' if i == 26 else ',' if i == 27 else '!' if i == 28 else chr(i + ord('a')) for i in (K_inv.dot(C) % 29).T.reshape(-1)])

def main():
  text = input("Enter the message:\t")
  key = input("Enter the key:\t\t")
  print("Key\t\t:\t", key, "\nOriginal Text\t:\t", text, '\n', '-' * 60, sep="")
  if(len(key) != 9):
    print("ValueError: Key Length should be of size 9")
    exit()

  cipher, length = encrypt(key, text)
  print("Cipher Text\t:\t", cipher, sep="")
  decipher = decrypt(key, cipher)
  print("Deciphered Text\t:\t", decipher, sep="")
  print("Original Text\t:\t", decipher[:length], sep="")

if __name__ == '__main__':
  main()