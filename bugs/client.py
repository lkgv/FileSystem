from settings import *
from sub_server import do_recvfile as get_file, send_to_server

def put_file (ip_address, port, md5) :
    if DEBUG_level > 2 :
        print('Send file %s to %s:%s.'%(md5, ip_address, port))
    sk = socket.socket()
    sk.connect((ip_address, port))
    if os.path.exists(md5) :
        data = open(md5, 'rb').read()
        cnt = (len(data) + max_word - 1) / max_word
        while True :
            try :
                sk.send(bytes(str(cnt), encoding=charset))
                extend_one_second()
                sk.sendall(data)
                extend_one_second()
                sk.send(keyword['file_end'])
                if DEBUG_level > 2 :
                    print('Send file %s finished.'%md5)
                res = sk.recv(max_word)
                if res == keyword['OK'] :
                    if DEBUG_level > 0 :
                        print('Send file %s accepted.'%md5)
                    break
                else :
                    if DEBUG_level > 1 :
                        print('Error: Send file %s checksum failed! Resend:'%md5)
            except :
                if DEBUG_level > 1 :
                    print('Error: Send file %s failed!'%md5)
    else :
        if DEBUG_level > 1 :
            print('Error: File %s not exists!'%md5)
    sk.close()


if __name__ == '__main__' :
    print('client main')