from backend.sql import *
from backend.settings import *
import random

socks = {}

def putsk (ip, sk) :
    global socks
    socks[ip] = sk

def find__children(db_name, folder_id):
    children = find_children(db_name, folder_id)
    print(len(str(children)))
    print(str(children))
    return str(children)


def get__father_folder(db_name, folder_id):
    father_folder = get_father_folder(db_name, folder_id)
    return str(father_folder)


def add__folder(db_name, folder_id, folder_name):
    message = add_folder(db_name, folder_id, folder_name)
    return message


def rename__file(db_name, file_id, new_name):
    message = rename_file(db_name, file_id, new_name)
    return message


def rename__folder(db_name, folder_id, new_name):
    message = rename_folder(db_name, folder_id, new_name)
    return message


def relink__folder(db_name, father_id, child_id):
    message = relink_folder(db_name, father_id, child_id)
    return message


def relink__document(db_name, folder_id, doc_id):
    message = relink_document(db_name, folder_id, doc_id)
    return message


def delete__folder(db_name, folder_id):
    message = delete_folder(db_name, folder_id)
    return message


def delete__file(db_name, doc_id):
    message = delete_file(db_name, doc_id)
    return message


def upload__file(db_name, folder_id, doc_name, doc_hash, doc_size, hash_table):
    doc_id = add_file(db_name, folder_id, doc_name, doc_hash, doc_size)
    servers = get_server(db_name)
    table = {}
    part = 0
    for hash in hash_table:
        print("hash", hash)
        part += 1
        ips = random.sample(servers, 2)
        print(ips)
        temp = []
        for ip in ips:
            tmp = ip
            print(type(ip["ip"]))
            sk = socks[ip['ip']]
            sk.send(keyword['getfile'])
            sk.send(bytes(hash, encoding=charset))
            res = sk.recv(max_word)
            if res == keyword['OK'] :
                port = int(str(sk.recv(max_word), encoding=charset).strip())
                tmp["port"] = port
                temp.append(tmp)
        table[hash] = temp
        add_package(db_name, doc_id, hash, part, ips)
    return str(table)


def download__file(db_name, doc_id):
    packages = find_package(db_name, doc_id)
    result = []
    for package in packages:
        tmp = package
        ips = get_ip(db_name, package["package_id"])
        for ip in ips:
            sk = socks[ip]
            sk.send(keyword['sendfile'])
            sk.send(bytes(package["package_hash"], encoding=charset))
            res = sk.recv(max_word)
            if res == keyword['OK'] :
                port = int(str(sk.recv(max_word), encoding=charset).strip())
                tmp["ip"] = ip
                tmp["port"] = port
                break
        result.append(tmp)
    return str(result)
