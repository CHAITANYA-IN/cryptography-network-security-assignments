import sys

OUTPUT_PATH = 'output.txt'
INPUT_PATH = 'input.txt'

stdout = sys.stdout
stdin = sys.stdin
sys.stdout = open(OUTPUT_PATH, 'w')
sys.stdin = open(INPUT_PATH)

verbose = ('-v' in sys.argv[2:]) or ('--verbose' in sys.argv[2:])
KEY_SIZE = 32
ENC_KEYS = []
DEC_KEYS = []
DEC_PER = [(24, 'M'), (25, 'A'), (26, 'A'), (27, 'M'), (22, 'N'), (23, 'N'), (18, 'M'), (19, 'A'), (20, 'A'), (21, 'M'), (16, 'N'), (17, 'N'), (12, 'M'), (13, 'A'), (14, 'A'), (15, 'M'), (10, 'N'), (11, 'N'), (6, 'M'), (7, 'A'), (8, 'A'), (9, 'M'), (4, 'N'), (5, 'N'), (0, 'M'), (1, 'A'), (2, 'A'), (3, 'M')]
shifts = [28, 24, 20, 16, 12, 8, 4, 0]
ADD_MOD = 16
MUL_MOD = 17
TEXT = []
STEPS = []
ROUNDS = 4
MUL_INV = {
  0:16, 1:1, 2:9, 3:6, 4:13, 5:7, 6:3, 7:5, 8:15, 9:2, 10:12, 11:14, 12:10, 13:4, 14:11, 15:8,
}
ADD_INV = {
  0:0, 1:15, 2:14, 3:13, 4:12, 5:11, 6:10, 7:9, 8:8, 9:7, 10:6, 11:5, 12:4, 13:3, 14:2, 15:1,
}

def mulMod(op1, op2):
  if(op1 == 0):
    op1 = 16
  if(op2 == 0):
    op2 = 16
  return ((op1 * op2) % MUL_MOD) & 0xF

def addMod(op1, op2):
  return ((op1 + op2) % ADD_MOD)

def binary(num):
  return bin(num).replace('0b', '').rjust(4, '0')

def keyGenerator(key):
  global ENC_KEYS, DEC_KEYS
  if(len(hex(key).replace('0x', '').rjust(8, '0')) != 8):
    return False
  ENC_KEYS += [(key >> i & 0xF) for i in shifts]
  key = 0xFFFFFFFF & (key << 6) | ((key & 0xFC000000) >> (KEY_SIZE - 6))
  ENC_KEYS += [(key >> i & 0xF) for i in shifts]
  key = 0xFFFFFFFF & (key << 6) | ((key & 0xFC000000) >> (KEY_SIZE - 6))
  ENC_KEYS += [(key >> i & 0xF) for i in shifts]
  key = 0xFFFFFFFF & (key << 6) | ((key & 0xFC000000) >> (KEY_SIZE - 6))
  ENC_KEYS += [(key >> i & 0xF) for i in shifts[:4]]
  if(verbose): print('ENC_KEYS = ', ENC_KEYS)
  for i, j in DEC_PER:
    if(j == 'M'):
      val = MUL_INV[ENC_KEYS[i]]
    if(j == 'A'):
      val = ADD_INV[ENC_KEYS[i]]
    if(j == 'N'):
      val = ENC_KEYS[i]
    DEC_KEYS.append(val)
  if(verbose): print('DEC_KEYS = ', DEC_KEYS)
  return True

def divideText(text):
  global TEXT
  TEXT = [(text >> i & 0xF) for i in shifts[4:]]
  if(verbose): print('Dividing Text = ', TEXT)
  return True

def mergeText():
  global TEXT
  X1, X2, X3, X4 = TEXT
  S1, S2, S3, S4 = shifts[4:]
  if(verbose): print('Text Ready = ', X1 << S1 | X2 << S2 | X3 << S3 | X4 << S4)
  return X1 << S1 | X2 << S2 | X3 << S3 | X4 << S4

def round(num, decrypt=False):
  if(decrypt):
    keys = DEC_KEYS
  else:
    keys = ENC_KEYS
  if(num < 1 or num > 4):
    if(verbose): print("Invalid round number")
    return False
  global TEXT
  X1, X2, X3, X4 = TEXT
  K1, K2, K3, K4, K5, K6 = keys[(num-1)*6:num*6]
  step1 = mulMod(X1, K1)
  step2 = addMod(X2, K2)
  step3 = addMod(X3, K3)
  step4 = mulMod(X4, K4)
  step5 = step1 ^ step3
  step6 = step2 ^ step4
  step7 = mulMod(step5, K5)
  step8 = addMod(step6, step7)
  step9 = mulMod(step8, K6)
  step10 = addMod(step7, step9)
  step11 = step1 ^ step9
  step12 = step3 ^ step9
  step13 = step2 ^ step10
  step14 = step4 ^ step10
  if(verbose): print("Step 1", binary(step1), sep="\t")
  if(verbose): print("Step 2", binary(step2), sep="\t")
  if(verbose): print("Step 3", binary(step3), sep="\t")
  if(verbose): print("Step 4", binary(step4), sep="\t")
  if(verbose): print("Step 5", binary(step5), sep="\t")
  if(verbose): print("Step 6", binary(step6), sep="\t")
  if(verbose): print("Step 7", binary(step7), sep="\t")
  if(verbose): print("Step 8", binary(step8), sep="\t")
  if(verbose): print("Step 9", binary(step9), sep="\t")
  if(verbose): print("Step 10", binary(step10), sep="\t")
  if(verbose): print("Step 11", binary(step11), sep="\t")
  if(verbose): print("Step 12", binary(step12), sep="\t")
  if(verbose): print("Step 13", binary(step13), sep="\t")
  if(verbose): print("Step 14", binary(step14), sep="\t")
  if(decrypt):
    TEXT = [step11, step13, step12, step14]
  else:
    TEXT = [step11, step13, step12, step14]
  if(verbose): print(f'Round {num} = ', TEXT)
  return True

def finalRound(decrypt=False):
  global TEXT
  if(decrypt):
    keys = DEC_KEYS
  else:
    keys = ENC_KEYS
  X1, X2, X3, X4 = TEXT
  K1, K2, K3, K4 = keys[-4:]
  step1 = mulMod(X1, K1)
  step2 = addMod(X2, K2)
  step3 = addMod(X3, K3)
  step4 = mulMod(X4, K4)
  if(verbose): print(f'{X1} * {K1} % 17 = {step1}')
  if(verbose): print(f'{X2} + {K2} % 16 = {step2}')
  if(verbose): print(f'{X3} + {K3} % 16 = {step3}')
  if(verbose): print(f'{X4} * {K4} % 17 = {step4}')
  TEXT = [step1, step2, step3, step4]
  if(verbose): print('Final Round = ', TEXT)
  return True

def ideAlgo(key, text, decrypt=False):
  if(len(ENC_KEYS) == 0):
    keyGenerator(key)
  divideText(text)
  for i in range(1, ROUNDS + 1):
    round(i, decrypt=decrypt)
  finalRound(decrypt=decrypt)
  return mergeText()

def encrypt(text, key):
  num = 0
  for i in key[:4]:
    num = (num << 8) | ord(i)
  cipherText = ""
  if(len(text) & 1):
    text += 'x'
  for i, j in zip(text[::2], text[1::2]):
    groupedText = ord(i) << 8 | ord(j)
    cipher = ideAlgo(num, groupedText, decrypt=False)
    byte1 = (cipher >> 8) & 0xFF
    byte2 = cipher & 0xFF
    cipherText += chr(byte1) + chr(byte2)
  return cipherText

def decrypt(cipherText, key):
  num = 0
  for i in key[:4]:
    num = (num << 8) | ord(i)
  decipherText = ""
  if(len(cipherText) & 1):
    cipherText += 'x'
  for i, j in zip(cipherText[::2], cipherText[1::2]):
    groupedText = ord(i) << 8 | ord(j)
    decipher = ideAlgo(num, groupedText, decrypt=True)
    byte1 = (decipher >> 8) & 0xFF
    byte2 = decipher & 0xFF
    decipherText += chr(byte1) + chr(byte2)
  return decipherText

def main():
  key = input('Enter the key: ') # E.g. - 'Üo?Y'
  if(len(key) < 4):
    print("Key should be 4 characters long")
    exit()
  text = input('Enter the text: ') # E.g. -'\x9c¬'
  print('')
  cipherText = encrypt(text, key)
  print('Cipher Text = ', cipherText)
  decipherText = decrypt(cipherText, key)
  print('Deciphered Text = ', decipherText)

main()

sys.stdin.close()
sys.stdout.close()
sys.stdin = stdin
sys.stdout = stdout
