import sys

stdout = sys.stdout
stdin = sys.stdin
sys.stdout = open('output.txt', 'w')
sys.stdin = open('input.txt')


IP = [1, 5, 2, 0, 3, 7, 4, 6]
IPI = [3, 0, 2, 4, 6, 1, 7, 5]
EP = [3, 0, 1, 2, 1, 2, 3, 0]
P10 = [2, 4, 1, 6, 3, 9, 0, 8, 7, 5]
P8 = [5, 2, 6, 3, 7, 4, 9, 8]
P4 = [1, 3, 2, 0]
S0 = [
    [1, 0, 3, 2, ],
    [3, 2, 1, 0, ],
    [0, 2, 1, 3, ],
    [3, 1, 3, 2, ],
]
S1 = [
    [0, 1, 2, 3, ],
    [2, 0, 1, 3, ],
    [3, 0, 1, 0, ],
    [2, 1, 0, 3, ],
]
K1 = ""
K2 = ""
dec2bin = {0: '00', 1: '01', 2: '10', 3: '11', }
bin2dec = {'00': 0, '01': 1, '10': 2, '11': 3, }


def lenCheck(l1: list, l2: list):
    return (len(l1) == len(l2))


def circularLeftShift(key: str, shift: int) -> str:
    if(len(key) != 10 or shift < 1):
        return None
    l = key[:5]
    r = key[5:]
    return l[shift:] + l[:shift] + r[shift:] + r[:shift]


def permutation(s: str, permutationArray: list) -> str:
    return ''.join([s[i] for i in permutationArray])


def xor(l1: list, l2: list) -> list:
    if(not(lenCheck(l1, l2))):
        return None
    return ''.join([str(int(not(l2[index] == ele))) for index, ele in enumerate(l1)])


def sBoxSubstitution(s: str, type: int) -> str:
    sBox = S0 if type == 0 else S1
    type *= 4
    print(f'dec2bin[sBox[bin2dec[s[{type+0}] + s[{type+3}]]][bin2dec[s[{type+1}] + s[{type+2}]]]]')
    print(f'dec2bin[sBox[bin2dec[{s[type+0]} + {s[type+3]}]][bin2dec[{s[type+1]} + {s[type+2]}]]]')
    print(f'dec2bin[sBox[{bin2dec[s[type+0] + s[type+3]]}][{bin2dec[s[type+1] + s[type+2]]}]]')
    print(f'dec2bin[{sBox[bin2dec[s[type+0] + s[type+3]]][bin2dec[s[type+1] + s[type+2]]]}]')
    return dec2bin[sBox[bin2dec[s[type+0] + s[type+3]]][bin2dec[s[type+1] + s[type+2]]]]


def LRDivider(s: str):
    if(len(s) != 8):
        return None
    return (str(s[:4]), str(s[4:]))


def switchHalves(s: str) -> str:
    if(len(s) != 8):
        return None
    return s[4:] + s[:4]


def keyGeneration(key: str):
    global K1, K2
    if(len(key) != 10):
        return None
    print('Original Key: ', key)
    P10Key = permutation(key, P10)
    print('Permutated Key(P10): ', P10Key)
    CLSKey1 = circularLeftShift(P10Key, 1)
    print('Shifting L and R to left by 1: ', CLSKey1)
    K1 = permutation(CLSKey1, P8)
    print('Key 1 using P8: ', K1)
    CLSKey2 = circularLeftShift(P10Key, 3)
    print('Shifting L and R to left by 2: ', CLSKey2)
    K2 = permutation(CLSKey2, P8)
    print('Key 2 using P8: ', K2)
    print('Key Generated\n', '-' * 40, sep="")


def mapping(text, key):
    l, r = LRDivider(text)
    print('Left Half: ', l)
    print('Right Half: ', r)
    expandedR = permutation(r, EP)
    print('Expanding right half: ', expandedR)
    Xored = xor(expandedR, key)
    print('Xoring the expanded right half: ', Xored)
    s0 = sBoxSubstitution(Xored, 0)
    print('Substitution Box 0: ', s0)
    s1 = sBoxSubstitution(Xored, 1)
    print('Substitution Box 1: ', s1)
    afterSubstitution = (s0 + s1)
    print('Concatenating: ', afterSubstitution)
    p4PermutatedR = permutation(afterSubstitution, P4)
    print('P4 permutation: ', p4PermutatedR)
    return (l, r, p4PermutatedR)


def Round(text, key):
    l, r, intermediate = mapping(text, key)
    Xored = xor(l, intermediate)
    print('Xoring the left part: ', Xored)
    return (Xored + r)


def encrypter(plainText: str) -> str:
    if(len(plainText) != 8):
        return None
    print('Plain Text: ', plainText)
    initialPer = permutation(plainText, IP)
    print('Initial Permutation: ', initialPer)
    output1 = Round(initialPer, K1)
    print('Round 1: ', output1)
    switched = switchHalves(output1)
    print('Switching L and R: ', switched)
    output2 = Round(switched, K2)
    print('Round 2: ', output2)
    cipherText = permutation(output2, IPI)
    print('Cipher generated: ', cipherText, '\nEncryption Successful\n', '-' * 40, sep='')
    return cipherText


def decrypter(cipherText: str) -> str:
    if(len(cipherText) != 8):
        return None
    print('Cipher Text: ', cipherText)
    initialPer = permutation(cipherText, IP)
    print('Initial Permutation: ', initialPer)
    output1 = Round(initialPer, K2)
    print('Round 1: ', output1)
    switched = switchHalves(output1)
    print('Switching L and R: ', switched)
    output2 = Round(switched, K1)
    print('Round 2: ', output2)
    plainText = permutation(output2, IPI)
    print('PlainText generated: ', plainText, '\nDecryption Successful\n', '-' * 40, sep='')
    return plainText


def convertBitString(text):
    cipherText = encrypter(text)
    print('\n\nCipher Text: ', repr(cipherText), "\n\n"+'-' * 50)
    decipherText = decrypter(cipherText)
    print('\n\nPlain Text: ', repr(decipherText), "\n\n"+'-' * 50)

def convertText(text):
    cipherText = ''
    plainText = ''
    for i in text:
        print('\n\nFor', i, ':')
        cipherText += chr(int(encrypter(bin(ord(i)).lstrip('0b').rjust(8, '0')), 2))
    print('\n\nCipher Text: ', repr(cipherText), "\n\n"+'-' * 50)
    for i in cipherText:
        plainText += chr(int(decrypter(bin(ord(i)).lstrip('0b').rjust(8, '0')), 2))
    print('\n\nPlain Text: ', repr(plainText), "\n\n"+'-' * 50)


def main():
    key = '1110001100'
    keyGeneration(key)
    text = input()
    if(text.isnumeric() and set(text) == {'0', '1'}):
        convertBitString(text)
    else:
        convertText(text)

main()

sys.stdin.close()
sys.stdout.close()
sys.stdin = stdin
sys.stdout = stdout
