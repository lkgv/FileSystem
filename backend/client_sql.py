from backend.client import call_server, put_file, get_file
from backend.settings import *

def find_children(db_name, folder_id):
    message = "find_children,"+db_name+","+str(folder_id)
    children = call_server(message)
    children = eval(children)
    return children


def get_father_folder(db_name, folder_id):
    message = "get_father_folder,"+db_name+","+str(folder_id)
    father_folder = call_server(message)
    father_folder = eval(father_folder)
    return father_folder


def add_folder(db_name, folder_id, folder_name):
    message = "add_folder,"+db_name+","+str(folder_id)+","+folder_name
    print(message)
    answer = call_server(message)
    return answer


def rename_file(db_name, file_id, new_name):
    message = "rename_file,"+db_name+","+str(file_id)+","+new_name
    answer = call_server(message)
    return answer


def rename_folder(db_name, folder_id, new_name):
    message = "rename_folder,"+db_name+","+str(folder_id)+","+new_name
    answer = call_server(message)
    return answer


def relink_folder(db_name, father_id, child_id):
    message = "relink_folder,"+db_name+","+str(father_id)+","+str(child_id)
    answer = call_server(message)
    return answer


def relink_document(db_name, folder_id, doc_id):
    message = "relink_document,"+db_name+","+str(folder_id)+","+str(doc_id)
    answer = call_server(message)
    return answer


def delete_folder(db_name, folder_id):
    message = "delete_folder,"+db_name+","+str(folder_id)
    answer = call_server(message)
    return answer


def delete_file(db_name, doc_id):
    message = "delete_file,"+db_name+","+str(doc_id)
    answer = call_server(message)
    return answer


def upload_file(db_name, folder_id, doc_name, doc_hash, doc_size, hash_table,
                pid, progress_sig, finish_sig):
    message = "upload_file,"+db_name+","+str(folder_id)+","+doc_name+","+doc_hash+","+str(doc_size)+","
    message += "|".join(hash_table)
    answer = call_server(message)
    answer = eval(answer)
    cnt = [len(answer)*2, threading.Lock()]
    def dosth (cnt) :
        cnt[1].acquire()
        cnt[0] -= 1
        ps = 1 - cnt[0] / len(answer) / 2
        progress_sig.emit(pid, ps)
        cnt[1].release()
    sth = lambda: dosth(cnt)
    for hash, table in answer.items():
        for tmp in table:
            ip = tmp["ip"]
            port = tmp["port"]
            newThread(put_file, args=[ip, port, hash, sth])
    while cnt[0] > 0:
        extend_one_second()
    finish_sig.emit(pid)
    return "upload file success"


def download_file(db_name, pid, doc_id, path, progress_sig, finish_sig):
    message = "download_file,"+db_name+","+str(doc_id)
    answer = call_server(message)
    answer = eval(answer)
    cnt = [len(answer), threading.Lock()]
    def dosth(cnt):
        cnt[1].acquire()
        cnt[0] -= 1
        ps = 1 - cnt[0] / len(answer)
        progress_sig.emit(pid, ps)
        cnt[1].release()
    sth = lambda: dosth(cnt)
    for package in answer:
        newThread(get_file, args=[package["ip"], package["port"], package["package_hash"], sth])
    while cnt[0] > 0:
        extend_one_second()
    sorted(answer, key=answer["part"])
    file = open(path, 'w')
    for package in answer:
        pack = open("tmp/"+package["package_hash"])
        data = pack.read()
        pack.close()
        file.write(data)
    file.close()
    finish_sig.emit(pid)
    return answer
