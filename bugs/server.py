from settings import *

def main (local_port = default_server_port) :
    try :
        server_sk = socket.socket()
        server_sk.bind((local_IP(), local_port))
        server_sk.listen(500)
        if DEBUG_level > 0 :
            print('Server initialized. Address %s:%s'%(local_IP(), local_port))
        while True:
            sk, addr = server_sk.accept()
            wd = sk.recv(max_word)
            print(wd, addr)
    except :
        if DEBUG_level > -1 :
            print('Cannot start server %s:%s!'%(local_IP(), local_port))
