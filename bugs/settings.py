import socket
import platform
import time
import threading
import queue
import hashlib
import os

DEBUG_level = 5
"""
level 0: No message.
level 1: Status message only.
level 2: Status message and Error message.
level 3: All mesages. 
level 4: Useless messages.
"""


def extend_one_second () :
    time.sleep(1)
def extend_heartbeat () :
    time.sleep(5)
default_server_port = 8080
max_word = 1024
charset = 'utf-8'
work_dir = 'data'

keyword = {'heartbeat': 'heartbeat',
           'sendfile': 'sendfile',
           'No such file': 'No such file',
           'OK': 'OK',
           'file_end': 'file_end',
           'recvfile': 'recvfile',
           'getfile': 'getfile',
           'file already exist': 'file already exist',
           'not ok': 'not ok',
           'file_list': 'file_list',
           'clean': 'clean',
           }




def newThread (fun, args = None) :
    if args :
        t = threading.Thread(target=fun, args=args)
    else :
        t = threading.Thread(target=fun)
    t.setDaemon(True)
    t.start()
def local_IP () :
    if platform.system() == 'Windows' :
        return socket.gethostbyname(socket.gethostname())
    else :
        return '127.0.0.1'
def conv (dic) :
    for it in dic.keys() :
        try :
            dic[it] = bytes(dic[it]+' '*(max_word - len(dic[it])), encoding=charset)
        except :
            pass

conv(keyword)