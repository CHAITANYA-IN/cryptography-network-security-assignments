def encrypt(text: str, key: str):
  """Function to encrypt the message using XOR Cipher"""
  """Converts the hex and xors the hex with key in repetative way later"""
  text = text.lower()
  key = key.lower()
  cipher = ""
  i = 0
  hexText = ''.join([hexer(ord(i)) for i in text])
  while(i < len(hexText)):
    letterOfText = ord(hexText[i])
    letterOfKey = (ord(key[i % len(key)]))
    encryptedForm = (letterOfText ^ letterOfKey)
    cipher += chr(encryptedForm)
    i += 1
  return cipher

def decrypt(cipher: str, key: str):
  """Function to decrypt the message"""
  """Xors the hex with key in repetative way and converts the hex later"""
  key = key.lower()
  text = ""
  i = 0
  while(i < len(cipher)):
    letterOfText = ord(cipher[i])
    letterOfKey = (ord(key[i % len(key)]))
    decryptedForm = (letterOfText ^ letterOfKey)
    text += chr(decryptedForm)
    i += 1
  deHexedText = ''.join([chr(dehexer(i+j)) for i,j in zip(text[::2], text[1::2])])
  return deHexedText

def hexer(n: int):
  return hex(n).lstrip('0x').rjust(2, '0')[::-1]

def dehexer(n: str):
  return int(n[::-1], 16)