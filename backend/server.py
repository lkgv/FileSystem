from backend.settings import *
from backend.server_sql import *

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
    message = message.split(",")
    if message[0] == "find_children":
        return find_children(message[1], int(message[2]))
    elif message[0] == "get_father_folder":
        return get_father_folder(message[1], int(message[2]))
    elif message[0] == "add_folder":
        return add_folder(message[1], int(message[2]), message[3])
    elif message[0] == "rename_file":
        return rename_file(message[1], int(message[2]), message[3])
    elif message[0] == "rename_folder":
        return rename_folder(message[1], int(message[2]), message[3])
    elif message[0] == "relink_folder":
        return relink_folder(message[1], int(message[2]), int(message[3]))
    elif message[0] == "relink_document":
        return relink_document(message[1], int(message[2]), int(message[3]))
    elif message[0] == "delete_folder":
        return delete_folder(message[1], int(message[2]))
    elif message[0] == "delete_file":
        return delete_file(message[1], int(message[2]))
    elif message[0] == "upload_file":
        return upload_file(message[1], int(message[2]), message[3], message[4], float(message[5]),
                           message[6].split("|"))
    elif message[0] == "download_file":
        return download_file(message[1], int(message[2]))
    else:
        return "The order is wrong!!!"


def server():
    while True:
        sk, addr = server_sk.accept()
        data = sk.recv(max_word)
        if data == keyword['link']:
            socks[addr[0]] = sk
            if DEBUG_level > 3 :
                print('Subserver - %s linked.'%addr[0])
        elif data == '':
            continue
        else:
            data = split_recv(sk)
            if data:
                if DEBUG_level > 3 :
                    print('Recv command:', data)
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

if __name__ == "__main__":
    print(local_IP())
    main()