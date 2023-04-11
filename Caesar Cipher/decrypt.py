def decrypt(cipherText: str) -> list:
  """
    Decrypts by shifting the cipher letters back by 1-26 possible shifts
  """
  decryptedForms = []
  plainText = ''
  for i in range(1, 27):
    plainText = ''
    for C in cipherText:
      if(ord(C) <= ord('z') and ord(C) >= ord('a')):
        plainText += chr(ord('a') + (ord(C) - ord('a') - i) % 26)
      elif(ord(C) <= ord('Z') and ord(C) >= ord('A')):
        plainText += chr(ord('A') + (ord(C) - ord('A') - i) % 26)
      else:
        plainText += " "
    decryptedForms.append(plainText)
  return decryptedForms

def decipherFormatter(decryptedForms: list, blockSize: int, lineBlocks: int) -> str:
  plainText = ''
  for index, cipher in enumerate(decryptedForms):
    blocks = 0
    plainText += f'Key {index + 1}:\n'
    for i, C in enumerate(cipher):
      if((i + 1) % blockSize):
        plainText += C
      else:
        blocks += 1
        if(blocks % lineBlocks):
          plainText += C + ' '
        else:
          plainText += C + '\n'
    plainText += '\n\n'
  return plainText