from backend.settings import *
from backend.sub_server import do_recvfile, send_to_server

server_sk = socket.socket()

def get_file(ip_address, port, md5, sth) :
    do_recvfile(ip_address, port, md5)
    sth()

def put_file(ip_address, port, md5, sth):
    if DEBUG_level > 2:
        print('Send file %s to %s:%s.' % (md5, ip_address, port))
    sk = socket.socket()
    sk.connect((ip_address, port))
    if os.path.exists(md5):
        file = open('tmp/'+md5, 'rb')
        data = file.read()
        file.close()
        cnt = (len(data) + max_word - 1) / max_word
        while True:
            try:
                sk.send(bytes(str(cnt), encoding=charset))
                extend_one_second()
                sk.sendall(data)
                extend_one_second()
                sk.send(keyword['file_end'])
                if DEBUG_level > 2:
                    print('Send file %s finished.' % md5)
                res = sk.recv(max_word)
                if res == keyword['OK']:
                    if DEBUG_level > 0:
                        print('Send file %s accepted.' % md5)
                    break
                else:
                    if DEBUG_level > 1:
                        print('Error: Send file %s checksum failed! Resend:' % md5)
            except:
                if DEBUG_level > 1:
                    print('Error: Send file %s failed!' % md5)
    else:
        if DEBUG_level > 1:
            print('Error: File %s not exists!' % md5)
    sk.close()
    sth()


def call_server(message):
    print(fill(bytes(str(len(message)), encoding=charset)))
    server_sk.send(fill(bytes(str(len(message)), encoding=charset)))
    print(message)
    server_sk.sendall(bytes(message, encoding=charset))
    return split_recv(server_sk)


def init(server_ip, server_port):
    global server_sk
    server_sk = socket.socket()
    server_sk.connect((server_ip, server_port))


if __name__ == '__main__':
    print('client main')
