class PlayFairCipher(object):
    """Encrypter based on Play Fair Classical Substitution Cipher Algorithm"""
    def __init__(self: object, plainText: str=None,
        cipherText: str=None, key: str= None) -> object:
        """Set parameters of playfair cipher"""
        super().__init__()
        self.setPlainText(plainText)
        self.setCipherText(cipherText)
        self._key = self.cleaner(key, True)
        if(self.isEmpty(self._cipherText)):
            self.encrypt()
            print(self)
        elif(self.isEmpty(self._plainText)):
            self.decrypt()
            print(self)
        else:
            self.encrypt()
            print('Results using the text entered: ', self)
            self.setCipherText(cipherText)
            self.decrypt()
            print('Results using the cipher entered: ', self)

    def setPlainText(self: object, plainText: str) -> None:
        """Set Plain Text"""
        self._plainText = self.textTokenizer(self.cleaner(plainText))

    def setCipherText(self: object, cipherText: str) -> None:
        """Set Cipher Text"""
        self._cipherText = self.textTokenizer(self.cleaner(cipherText))

    def isEmpty(self: object, s: str) -> bool:
        """Check the string is empty or null"""
        return (s == '' or s == None)

    def setMatrix(self: object, value: object = 0) -> None:
        """Initialize 5 x 5 Key Matrix"""
        self.matrix = [[value for _ in range(5)] for _ in range(5)]

    def getMatrix(self: object) -> None:
        """Print Key Matrix"""
        print("Key Matrix:")
        for l in self.matrix:
            print(*l, sep=" ")

    def __str__(self: object) -> str:
        """Shown on printing the object"""
        return f'{self.__class__.__name__}(Key={self._key}, PlainText={self._plainText}, CipherText={self._cipherText})'

    def cleaner(self: object, text: str, isKey: bool = False) -> str:
        """Removes non-alphabetic characters"""
        import re
        s = re.sub('[^A-Za-z]+', '', text).upper()
        return s.replace('J', 'I')# if isKey else s

    def textTokenizer(self: object, s: str) -> str:
        """Prepare text by adding dummy characters"""
        for i in range(0, len(s) + 1, 2):
            if(i < len(s) - 1 and s[i] == s[i + 1]):
                s = s[:i+1] + 'X' + s[i+1:]
        return s + ('X' if (len(s) & 1 == 1) else '')

    def putCharactersInList(self: object) -> list:
        """Prepare the list of values to be added in key matrix"""
        charactersInKey = []
        charactersLeft = [chr(ord('A') + i) for i in range(0, 26)]
        charactersLeft.remove('J')
        for c in self._key:
            if c in charactersLeft:
                charactersLeft.remove(c)
            if c not in charactersInKey:
                charactersInKey.append(c)
        return charactersInKey + charactersLeft

    def createMatrix(self: object) -> None:
        """Set the key matrix"""
        self.setMatrix(None)
        l = self.putCharactersInList()
        for i in range(5):
            for j in range(5):
                self.matrix[i][j] = l[i*5+j]
        self.getMatrix()

    def index(self: object, c: str) -> tuple:
        """Index of element in key matrix"""
        for i, l in enumerate(self.matrix):
            for j, ele in enumerate(l):
                if c == ele:
                    return (i, j)

    def diagraphEncrypter(self: object, diagraph: str) -> str:
        """Encrypt the diagraph as per rules of playfair cipher"""
        pos1 = self.index(diagraph[0])
        pos2 = self.index(diagraph[1])
        if pos1[1] == pos2[1]:
            return f'{self.matrix[(pos1[0]+1) % 5][pos1[1]]}{self.matrix[(pos2[0]+1) % 5][pos2[1]]}'
        elif pos1[0] == pos2[0]:
            return f'{self.matrix[pos1[0]][(pos1[1]+1) % 5]}{self.matrix[pos2[0]][(pos2[1]+1) % 5]}'
        else:
            return f'{self.matrix[pos1[0]][pos2[1]]}{self.matrix[pos2[0]][pos1[1]]}'

    
    def diagraphDecrypter(self: object, diagraph: str) -> str:
        """Decrypt the diagraph as per rules of playfair cipher"""
        pos1 = self.index(diagraph[0])
        pos2 = self.index(diagraph[1])
        if pos1[1] == pos2[1]:
            return f'{self.matrix[(pos1[0]-1) % 5][pos1[1]]}{self.matrix[(pos2[0]-1) % 5][pos2[1]]}'
        elif pos1[0] == pos2[0]:
            return f'{self.matrix[pos1[0]][(pos1[1]-1) % 5]}{self.matrix[pos2[0]][(pos2[1]-1) % 5]}'
        else:
            return f'{self.matrix[pos1[0]][pos2[1]]}{self.matrix[pos2[0]][pos1[1]]}'

    def encrypt(self: object) -> str:
        """Prepare the cipher text for given plain text"""
        print("Encrypting...")
        self._cipherText = ""
        self.createMatrix()
        i = 0
        while(i < len(self._plainText)):
            self._cipherText += f'{self.diagraphEncrypter(self._plainText[i:i+2])}'
            i += 2
        return self._cipherText
    
    def decrypt(self):
        """Prepare the plain text for given cipher text"""
        print("Decrypting...")
        self._plainText = ""
        self.createMatrix()
        i = 0
        while(i < len(self._cipherText)):
            self._plainText += f'{self.diagraphDecrypter(self._cipherText[i:i+2])}'
            i += 2
        return self._plainText


def main():
    PFC = PlayFairCipher(input('Enter Plain Text: '), input('Enter Cipher Text: '), input('Enter Key: '))

if __name__ == '__main__':
    main()