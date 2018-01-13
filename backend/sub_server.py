from backend.settings import *

port_queue = queue.Queue()
command_list = queue.Queue()
server_sk = socket.socket()
sockets = {}
file_hash = 0


def update_hash(md5):
    for ch in md5:
        if ch not in '1234567890abcdefABCDEF':
            if DEBUG_level > 1:
                print('Error: Incorrect md5 value: %s' % md5)
            return
    global file_hash
    file_hash = file_hash ^ eval('0x' + md5)


def subserver_init(port_range):
    if DEBUG_level > 0:
        print('Starting sockets.')
    for pt in port_range:
        try:
            sk = socket.socket()
            sk.bind((local_IP(), pt))
            sk.listen(5)
            port_queue.put(pt)
            sockets[pt] = sk
        except:
            if DEBUG_level > 1:
                print('Error: Cannot start server on port %d!' % pt)

    os.chdir(work_dir)
    for file_name in os.listdir('.'):
        update_hash(file_name)

    if DEBUG_level > 0:
        print('Server started. Total ports: %d.' % port_queue.qsize())


def send(ip, port, message):
    if DEBUG_level > 2:
        print('Send', message, 'to %s:%d.' % (ip, port))
    while True:
        try:
            sk = socket.socket()
            sk.connet((ip, port))
            sk.sendall(message)
            if DEBUG_level > 2:
                print('Send succeed.')
            break
        except:
            if DEBUG_level > 1:
                print('Error: Cannot send', message, 'to %s:%d!' % (ip, port))
        extend_one_second()
    try:
        sk.close()
    except:
        pass


def send_to_server(message):
    if DEBUG_level > 2:
        print('Send', message, 'to server.')
    while True:
        try:
            server_sk.sendall(message)
            if DEBUG_level > 2:
                print('Send succeed.')
            break
        except:
            if DEBUG_level > 1:
                print('Error: Cannot send', message, 'to server!')


def heartbeat():
    while True:
        try:
            if DEBUG_level > 3:
                #print('Send heartbeat.')
                pass
            # send_to_server(keyword['heartbeat'])
            # send_to_server(bytes('%032x'%file_hash, encoding=charset))
        except:
            if DEBUG_level > 1:
                print('Error: Cannot send heartbeats!')
        extend_heartbeat()


def recv_command():
    while True:
        command = server_sk.recv(max_word)
        if DEBUG_level > 2:
            print('Get command:', command)
        command_list.put(command)


def do_sendfile(local_port, md5):
    if DEBUG_level > 2:
        print('Send file %s to port %d.' % (md5, local_port))
    local_sk = sockets[local_port]
    if os.path.exists(md5):
        send_to_server(keyword['OK'])
        send_to_server(bytes(local_port, encoding=charset))
        data = open(md5, 'rb').read()
        while True:
            try:
                sk, addr = local_sk.accept()
                sk.send(fill(bytes(str(len(data)), encoding=charset)))
                sk.sendall(data)
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
        send_to_server(keyword['No such file'])
    port_queue.put(local_port)


def do_recvfile(ip_address, port, md5):
    if DEBUG_level > 2:
        print('Recv file %s from %s:%d.' % (md5, ip_address, port))
    exist_flag = False
    if os.path.exists(md5):
        send_to_server(keyword['file already exist'])
        if DEBUG_level > 1:
            print('Error: File %s already exists!' % md5)
        exist_flag = True
    else:
        send_to_server(keyword['OK'])

    while True:
        try:
            sk = socket.socket()
            sk.connect((ip_address, port))
            data = split_recv(sk)

            if exist_flag:
                sk.send(keyword['OK'])
                sk.close()
                break
            elif md5 == hashlib.md5(data).hexdigest():
                file = open(md5, 'wb')
                file.write(data)
                file.close()
                sk.send(keyword['OK'])
                sk.close()
                if DEBUG_level > 2:
                    print('Recv file %s from %s:%d succeed.' % (md5, ip_address, port))
                update_hash(md5)
                break
            else:
                if DEBUG_level > 1:
                    print('Error: Recv file %s from %s:%d Hash Error!' % (md5, ip_address, port))
                sk.send(keyword['not ok'])
        except:
            if DEBUG_level > 1:
                print('Error: Recv file %s from %s:%d failed!' % (md5, ip_address, port))
            send(ip_address, port, keyword['not ok'])
    try:
        sk.close()
    except:
        pass


def do_getfile(local_port, md5):
    if DEBUG_level > 2:
        print('Get file %s from port %d.' % (md5, local_port))
    local_sk = sockets[local_port]
    exist_flag = False
    if os.path.exists(md5):
        send_to_server(keyword['file already exist'])
        if DEBUG_level > 1:
            print('Error: File %s already exists!' % md5)
        exist_flag = True
    else:
        send_to_server(keyword['OK'])
        send_to_server(bytes(str(local_port), encoding=charset))

    while True:
        try:
            sk, address = local_sk.accept()
            data = split_recv(sk)

            if exist_flag:
                sk.send(keyword['OK'])
                break
            elif md5 == hashlib.md5(data).hexdigest():
                file = open(md5, 'wb')
                file.write(data)
                file.close()
                sk.send(keyword['OK'])
                if DEBUG_level > 2:
                    print('Get file %s from port %d succeed.' % (md5, local_port))
                update_hash(md5)
                break
            else:
                if DEBUG_level > 1:
                    print('Error: Get file %s from port %d Hash Error!' % (md5, local_port))
                sk.send(keyword['not ok'])
        except:
            if DEBUG_level > 1:
                print('Error: Get file %s from port %d failed!' % (md5, local_port))

    port_queue.put(local_port)


def get_command():
    flag = True
    while command_list.empty():
        extend_one_second()
        if DEBUG_level > 3:
            if flag :
                print('Waiting for commands...')
            flag = False
    return command_list.get()


def send_file_list():
    lst = os.listdir('.')
    send_to_server(bytes(str(len(lst)), encoding=charset))
    for md5 in os.listdir('.'):
        md5 = md5 + ' ' * (max_word - len(md5))
        send_to_server(bytes(md5, encoding=charset))


def do_clean():
    global file_hash
    file_hash = 0
    for md5 in os.listdir('.'):
        os.remove(md5)


def sub_server():
    newThread(recv_command)
    while True:
        command = get_command()
        if DEBUG_level > 2:
            print('Do command:', command)
        if command == keyword['sendfile']:
            md5 = str(get_command(), encoding=charset)
            local_port = port_queue.get()
            if DEBUG_level > 2:
                print('Send file %s from port %d.' % (md5, local_port))
            newThread(do_sendfile, args=[local_port, md5])
        elif command == keyword['recvfile']:
            ip_address = str(get_command(), encoding=charset)
            port = int(str(get_command(), encoding=charset))
            md5 = str(get_command(), encoding=charset)
            if DEBUG_level > 2:
                print('Recv file %s from %s:%d.' % (md5, ip_address, port))
            newThread(do_recvfile, args=[ip_address, port, md5])
        elif command == keyword['getfile']:
            md5 = str(get_command(), encoding=charset)
            local_port = port_queue.get()
            if DEBUG_level > 2:
                print('Get file %s from port %d.' % (md5, local_port))
            newThread(do_getfile, args=[local_port, md5])
        elif command == keyword['file_list']:
            if DEBUG_level > 2:
                print('Send file list to server twice.')
            send_file_list()
            send_file_list()
        elif command == keyword['clean']:
            if DEBUG_level > 2:
                print('Clean local files.')
            do_clean()
        else:
            if DEBUG_level > 1:
                print('Error: Undefined command:', command)


def main(server_ip, server_port=default_server_port, local_port_range=range(8088, 8188)):
    try:
        server_sk.connect((server_ip, server_port))
        send_to_server(b'1024'+b' '*(max_word - 4))
        send_to_server(keyword['link'])
    except:
        if DEBUG_level > -1:
            print('Error! Cannot connect to server %s:%d!' % (server_ip, server_port))
        return

    newThread(heartbeat)
    subserver_init(local_port_range)

    if port_queue.qsize() > 0:
        if DEBUG_level > 0:
            print('Sub server initialized.')
        sub_server()
    else:
        if DEBUG_level > -1:
            print('Error! Cannot open sub_server ports!')


if __name__ == '__main__':
    server_ip = '192.168.1.138' #input('Input server\'s IP address:')
    thread_cnt = '' #input('Input the number of maximum threads(default 100):')
    if thread_cnt == '':
        thread_cnt = 100
    else:
        thread_cnt = int(thread_cnt)
    main(server_ip, local_port_range=range(8088, 8088 + thread_cnt))
