import encrypt, decrypt

def __main__():
  # Initializing variables for encryption
  numberOfLetters = 26
  plainText = ''
  cipher = ''

  # Getting required user inputs
  key = int(input('Enter the key: '))
  messageFile = input('Enter the name of the file containing the message: ')

  # Reading the message to be encrypted
  try:
    f = open(messageFile, 'r')
    plainText = f.read()
  except:
    pass

  # Printing the clean formatted form of the message to be encrypted
  print(f'Message in {messageFile} to be encrypted:')
  print(encrypt.textFormatter(plainText, 5, 10), end="\n\n")

  # Printing the encrypted message
  cipher = encrypt.encrypt(plainText, key, numberOfLetters)
  print(f'Encryption of the message')
  print(encrypt.cipherFormatter(cipher, 5, 10), end="\n\n")

  # Printing the decrypted messages using all possible keys
  print(f'\n\nDecryption of the above cipher for keys 1 to 27:\n')
  decipherForm = decrypt.decrypt(cipher)
  print(decrypt.decipherFormatter(decipherForm, 5, 10), end="\n\n")

if __name__ == '__main__':
  __main__()