from backend.settings import *
import backend.server
import backend.sub_server


def fuck():
    while True:
        print(sk2.recv(1024))


sk0 = socket.socket()
sk1 = socket.socket()
sk0.bind(('127.0.0.1', 8080))
sk0.listen(5)
sk1.connect(('127.0.0.1', 8080))
sk2, fff = sk0.accept()
sk1.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sk2.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 2)
sk1.settimeout(0)
s = bytes('12345', encoding=charset)
# newThread(fuck)
sk1.send(s)
time.sleep(1)
sk1.send(s)
time.sleep(1)
sk1.send(s)
print(sk2.recv(1024))
print(sk2.recv(1024))
while True:
    print(sk2.recv(1024))

newThread(server.main)
extend_one_second()
sub_server.main(local_IP())
