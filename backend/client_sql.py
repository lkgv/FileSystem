from backend.client import call_server


def find_children(db_name, folder_id):
    message = "find_children,"+db_name+","+folder_id
    children = call_server(message)
    children = eval(children)
    return children


def get_father_folder(db_name, folder_id):
    message = "get_father_folder,"+db_name+","+folder_id
    father_folder = call_server(message)
    father_folder = eval(father_folder)
    return father_folder


def add_folder(db_name, folder_id, folder_name):
    message = "add_folder,"+db_name+","+folder_id+","+folder_name
    answer = call_server(message)
    return answer


def rename_file(db_name, file_id, new_name):
    message = "rename_file,"+db_name+","+file_id+","+new_name
    answer = call_server(message)
    return answer


def rename_folder(db_name, folder_id, new_name):
    message = "rename_folder,"+db_name+","+folder_id+","+new_name
    answer = call_server(message)
    return answer


def relink_folder(db_name, father_id, child_id):
    message = "relink_folder,"+db_name+","+father_id+","+child_id
    answer = call_server(message)
    return answer


def relink_document(db_name, folder_id, doc_id):
    message = "relink_document,"+db_name+","+folder_id+","+doc_id
    answer = call_server(message)
    return answer


def delete_folder(db_name, folder_id):
    message = "delete_folder,"+db_name+","+folder_id
    answer = call_server(message)
    return answer


def delete_file(db_name, doc_id):
    message = "delete_file,"+db_name+","+doc_id
    answer = call_server(message)
    return answer


def upload_file(db_name, folder_id, doc_name, doc_hash, doc_size):
    message = "upload_file,"+db_name+","+folder_id+","+doc_name+","+doc_hash+","+doc_size
    answer = call_server(message)
    return answer


def download_file(db_name, doc_id, path):
    message = "download_file,"+db_name+","+doc_id
    answer = call_server(message)
    answer = eval(answer)
    return answer
