from termcolor import colored
import argparse
import json
import requests
	
class Censys:

	def __init__(self, ip):

		self.API_URL = "https://www.censys.io/api/v1"
		self.UID = "YOUR_UID_HERE"
		self.SECRET = "YOUR_SECRET_HERE"
		self.ip = ip

	def search(self):

		pages = float('inf')
		page = 1

		while page <= pages:

			params = {'query' : self.ip, 'page' : page}
			res = requests.post(self.API_URL + "/search/ipv4", json = params, auth = (self.UID, self.SECRET))
			payload = res.json()

			for r in payload['results']:

				ip = r["ip"]
				proto = r["protocols"]
			
				print '[%s] IP: %s - Protocols: %s' % (colored('*', 'green'), ip, proto)
				
				if '80/http' in proto:
					self.view(ip)

			pages = payload['metadata']['pages']
			page += 1

	def view(self, server):

		res = requests.get(self.API_URL + ("/view/ipv4/%s" % server), auth = (self.UID, self.SECRET))
		payload = res.json()		

		try:
			if 'title' in payload['80']['http']['get'].keys():
				print "[+] Title: %s" % payload['80']['http']['get']['title']
			if 'server' in payload['80']['http']['get']['headers'].keys():
				print "[+] Server: %s" % payload['80']['http']['get']['headers']['server']
		except Exception as error:
			print error
		print ""

parser = argparse.ArgumentParser(description = 'CENSYS.IO Web Server Search')
parser.add_argument('-r', '--range', help='IPv4 Address Range', required = True)

args = parser.parse_args()
ip = args.range

censys = Censys(ip)
censys.search()
