def textFormatter(plainText: str, blockSize: int, lineBlocks: int) -> str:
  cleanText = ''
  blocks = 0
  index = 0
  for p in plainText:
    if((ord(p) <= ord('z') and ord(p) >= ord('a')) 
      or (ord(p) <= ord('Z') and ord(p) >= ord('A'))):
      if((index + 1) % blockSize):
        cleanText += p
      else:
        blocks += 1
        if(blocks % lineBlocks):
          cleanText += p + ' '
        else:
          cleanText += p + '\n'
      index += 1
  return cleanText

def encrypt(plainText: str, key: int, n: int) -> list:
  cipher = []
  for p in plainText:
    if(ord(p) <= ord('z') and ord(p) >= ord('a')):
      cipher.append(chr(ord('a') + (ord(p) - ord('a') + key) % n))
    if(ord(p) <= ord('Z') and ord(p) >= ord('A')):
      cipher.append(chr(ord('A')+ (ord(p) - ord('A') + key) % n))
  return cipher

def cipherFormatter(cipher: list, blockSize: int, lineBlocks: int) -> str:
  cipherText = ''
  blocks = 0
  for index, C in enumerate(cipher):
    if((index + 1) % blockSize):
      cipherText += C
    else:
      blocks += 1
      if(blocks % lineBlocks):
        cipherText += C + ' '
      else:
        cipherText += C + '\n'
  return cipherText
