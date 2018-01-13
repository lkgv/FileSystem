from backend.settings import *

server_sk = socket.socket()

def get_file(ip_address, port, md5, sth) :
    print('get', ip_address, port, md5)
    if DEBUG_level > 2:
        print('Recv file %s from %s:%d.' % (md5, ip_address, port))
    exist_flag = False
    if os.path.exists('tmp/'+md5):
        if DEBUG_level > 1:
            print('Error: File %s already exists!' % md5)
        exist_flag = True

    while True:
        try:
            print(ip_address, port)
            sk = socket.socket()
            sk.connect((ip_address, port))
            data = split_recv_b(sk)
            print(len(data))

            if exist_flag:
                sk.send(keyword['OK'])
                sk.close()
                break
            elif md5 == hashlib.md5(data).hexdigest():
                file = open('tmp/'+md5, 'wb')
                file.write(data)
                file.close()
                sk.send(keyword['OK'])
                sk.close()
                if DEBUG_level > 2:
                    print('Recv file %s from %s:%d succeed.' % (md5, ip_address, port))
                break
            else:
                if DEBUG_level > 1:
                    print('Error: Recv file %s from %s:%d Hash Error!' % (md5, ip_address, port))
                    print(md5, hashlib.md5(data).hexdigest())
                sk.send(keyword['not ok'])
        except Exception as e:
            print(e)
            if DEBUG_level > 1:
                print('Error: Recv file %s from %s:%d failed!' % (md5, ip_address, port))
            sk = socket.socket()
            sk.connect((ip_address, port))
            sk.send(keyword['not ok'])
    try:
        sk.close()
    except:
        pass
    sth()

def put_file(ip_address, port, md5, sth):
    print('put', ip_address, port, md5)
    if DEBUG_level > 2:
        print('Send file %s to %s:%s.' % (md5, ip_address, port))
    if os.path.exists('tmp/'+md5):
        file = open('tmp/'+md5, 'rb')
        data = file.read()
        file.close()
        cnt = len(data)
        while True:
            try:
                sk = socket.socket()
                sk.connect((ip_address, port))
                sk.send(bytes(str(cnt), encoding=charset))
                extend_one_second()
                sk.sendall(data)
                extend_one_second()
                sk.send(keyword['file_end'])
                if DEBUG_level > 2:
                    print('Send file %s finished.' % md5)
                res = sk.recv(max_word)
                sk.close()
                if res == keyword['OK']:
                    if DEBUG_level > 0:
                        print('Send file %s accepted.' % md5)
                    break
                else:
                    if DEBUG_level > 1:
                        print('Error: Send file %s checksum failed! Resend:' % md5)
            except Exception as e:
                print(e)
                if DEBUG_level > 1:
                    print('Error: Send file %s failed!' % md5)
    else:
        if DEBUG_level > 1:
            print('Error: File %s not exists!' % md5)
    sth()


def call_server(message):
    init('192.168.1.138',8080)
    print(fill(bytes(str(len(message)), encoding=charset)))
    server_sk.send(fill(bytes(str(len(message)), encoding=charset)))
    print(message)
    server_sk.sendall(bytes(message, encoding=charset))
    ret = split_recv(server_sk)
    print(ret)
    return ret


def init(server_ip, server_port):
    global server_sk
    server_sk = socket.socket()
    server_sk.connect((server_ip, server_port))


if __name__ == '__main__':
    print('client main')
