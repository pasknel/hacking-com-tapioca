from scapy.all import *

ipv6 = IPv6(dst = 'ff02::1')
icmpv6 = ICMPv6EchoRequest()
pacote = ipv6 / icmpv6

sucesso, falha = sr(pacote, timeout = 10, multi = True, iface = 'eth0')

for (requisicao, resposta) in sucesso:
	print "[+] Host: %s" % resposta[IPv6].src


