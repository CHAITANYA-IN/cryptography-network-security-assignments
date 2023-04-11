import socket, crypter

PORT = 2048
HOST = '127.0.0.1'
KEY = "ZEPLIN"

# Created socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket created successfully")

# Binding socket to specified port
s.bind((HOST, PORT))
print(f"Socket binded to port-{PORT} on host-{HOST}")

# Listening for connections
s.listen(5)
print("Socket is listening")

while (input('Do you want to keep the server alive? [Y/n]: ').upper() == 'Y'):
	print('Waiting for connections ...')
	# Get connection socket
	c, addr = s.accept()
	print(f"{addr} connected!")
	try:
		# Retrieve password
		encryptedText = c.recv(1024).decode()
		print(f'Password received: {repr(encryptedText)}')
		print(f'Decrypted Password: {crypter.decrypt(encryptedText, KEY)}')
	except:
		# Send authentication results back
		c.send(crypter.encrypt("Server Failed", KEY).encode())
	else:
		# Send authentication results back
		c.send(crypter.encrypt("Password sent successfully", KEY).encode())
	print(f'Closing connection with {addr}')
	#  Closing Connection socket
	c.close()

# Closing main socket
s.close()