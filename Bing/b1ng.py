import time
import random
import httplib

# CIDR Magic
from netaddr import *

# Bibliotecas HTTP
from BeautifulSoup import BeautifulSoup
from urllib2 import urlopen, Request
from urllib import urlencode

# Import graphviz
import sys
sys.path.append('..')
sys.path.append('/usr/lib/graphviz/python/')
sys.path.append('/usr/lib64/graphviz/python/')
import gv

# Import pygraph
from pygraph.classes.graph import graph
from pygraph.classes.digraph import digraph
from pygraph.algorithms.searching import breadth_first_search
from pygraph.readwrite.dot import write

RANGE = '200.181.29.0/26'

###################################################################################

def search(ip, gr):

	# REQUEST

	url = "http://br.bing.com/search?q=ip:%s" % ip
	headers = {'User-Agent' : 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:17.0) Gecko/20100101 Firefox/17.0'}
	req = Request(url, None, headers)
	request = urlopen(req)	

	# BEAUTIFUL SOUP

	html = request.read()		
	soup = BeautifulSoup(html)
	results = soup.findAll('div', attrs={"class" : "sa_mc"})
	
	# FILTRANDO RESULTADOS

	if len(results) > 0:

	        print "[*] IP: %s" % ip

		gr.add_node(ip)
		gr.add_edge((ip, RANGE))

		for result in results:

			# Parsing do HTML
			link = result.find('div', attrs={'class' : 'sb_tlst'})
			link = link.find('a')
			descricao = result.find('p')

			# Pegando o nome do host
			href = link['href']
			if 'http://' in href:
				href = href.replace('http://', '')
			else:
				href = href.replace('https://', '')
			
			# Adicionando host no grafo
			host = href[ : href.index('/')]
			if not gr.has_node(host):
				gr.add_node(host)
				gr.add_edge((host, ip))	
	
			print '\t[+] URL: %s' % href
			#if descricao:
			#	print '\t[+] Descricao: %s' % descricao.string
			print ''

	# Dormindo um pouco para evitar bloqueios
	time.sleep(5)

# Criando grafo
gr = graph()
gr.add_node(RANGE)

# Pegando ips
ips = IPSet([RANGE])

todos = []
for ip in ips:
	todos.append(ip)

# Fazendo shuffle
random.shuffle(todos)
for ip in todos:
	try:
		search(str(ip), gr)
	except httplib.IncompleteRead:
		print "[!] Erro httplib.IncompleteRead: IP (%s)" % ip		

st, order = breadth_first_search(gr, root=RANGE)
gst = digraph()
gst.add_spanning_tree(st)
dot = write(gst)
gvv = gv.readstring(dot)
gv.layout(gvv,'dot')
gv.render(gvv,'png','bing.png')	
