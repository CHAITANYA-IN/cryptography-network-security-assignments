import socket, crypter

HOST = '127.0.0.1'
PORT = 2048
KEY = "ZEPLIN"

# Connection socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created successfully')

# Connect to server
s.connect((HOST, PORT))
print(f'Connected to {HOST} on {PORT}')

# Send password to server
encryptedText = crypter.encrypt(input('Enter the password : '), KEY)
print(f'Encrypted Password: ', repr(encryptedText))
s.send(encryptedText.encode())

# Decrypt the authentication result
print(crypter.decrypt(s.recv(1024).decode(), KEY).capitalize())

