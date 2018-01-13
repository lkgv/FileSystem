from backend.settings import *

server_sk = socket.socket()
socks = {}


def server_gay_server(server1, server2, md5):
    md5 = bytes(md5, encoding=charset)
    sk1 = socks[server1]
    sk1.send(keyword['sendfile'])
    sk1.send(md5)
    res = sk1.recv(1024)
    if res == keyword['OK']:
        port = sk1.recv(1024)
        sk2 = socks[server2]
        sk2.send(keyword['recvfile'])
        sk2.send(fill(bytes(server1, encoding=charset)))
        sk2.send(fill(bytes(port, encoding=charset)))
        sk2.send(md5)
        res = sk2.recv(1024)
        if res == keyword['OK']:
            return 0
        if DEBUG_level > 1:
            print('File already exists')
        return 0
    if DEBUG_level > 1:
        print('No such file!')
    return -1


def server_gay_client(server, client_sk, md5):
    md5 = bytes(md5, encoding=charset)
    sk1 = socks[server]
    sk1.send(keyword['sendfile'])
    sk1.send(md5)
    res = sk1.recv(1024)
    if res == keyword['OK']:
        port = sk1.recv(1024)
        sk2 = client_sk
        sk2.send(keyword['getfile'])
        sk2.send(fill(bytes(server, encoding=charset)))
        sk2.send(fill(bytes(port, encoding=charset)))
        sk2.send(md5)
        res = sk2.recv(1024)
        if res == keyword['OK']:
            return 0
        if DEBUG_level > 1:
            print('File already exists')
        return 0
    if DEBUG_level > 1:
        print('No such file!')
    return -1


def client_gay_server(client_sk, server, md5):
    md5 = bytes(md5, encoding=charset)
    sk1 = socks[server]
    sk1.send(keyword['getfile'])
    sk1.send(md5)
    res = sk1.recv(1024)
    if res == keyword['OK']:
        port = sk1.recv(1024)
        sk2 = client_sk
        sk2.send(keyword['putfile'])
        sk2.send(fill(bytes(server, encoding=charset)))
        sk2.send(fill(bytes(port, encoding=charset)))
        sk2.send(md5)
        res = sk2.recv(1024)
        if res == keyword['OK']:
            return 0
        if DEBUG_level > 1:
            print('File already exists')
        return 0
    if DEBUG_level > 1:
        print('No such file!')
    return -1


def make(client, message):
    return 'What?'


def server():
    while True:
        sk, addr = server_sk.accept()
        data = sk.recv(max_word)
        if data == keyword['link']:
            socks[addr[0]] = sk
        elif data == '':
            continue
        else:
            data = split_recv(sk)
            if data:
                res = make(sk, data)
                if res:
                    sk.send(fill(bytes(str(len(res)), encoding=charset)))
                    sk.sendall(bytes(res, encoding=charset))
        extend_one_second()


def main(local_port=default_server_port):
    try:
        server_sk.bind((local_IP(), local_port))
        server_sk.listen(500)
        if DEBUG_level > 0:
            print('Server initialized. Address %s:%s' % (local_IP(), local_port))
        server()
    except:
        if DEBUG_level > -1:
            print('Cannot start server %s:%s!' % (local_IP(), local_port))
