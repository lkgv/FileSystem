from backend.sql import *


def find_children(db_name, folder_id):
    children = find_children(db_name, folder_id)
    return str(children)


def get_father_folder(db_name, folder_id):
    father_folder = get_father_folder(db_name, folder_id)
    return str(father_folder)


def add_folder(db_name, folder_id, folder_name):
    message = add_folder(db_name, folder_id, folder_name)
    return message


def rename_file(db_name, file_id, new_name):
    message = rename_file(db_name, file_id, new_name)
    return message


def rename_folder(db_name, folder_id, new_name):
    message = rename_folder(db_name, folder_id, new_name)
    return message


def relink_folder(db_name, father_id, child_id):
    message = relink_folder(db_name, father_id, child_id)
    return message


def relink_document(db_name, folder_id, doc_id):
    message = relink_document(db_name, folder_id, doc_id)
    return message


def delete_folder(db_name, folder_id):
    message = delete_folder(db_name, folder_id)
    return message


def delete_file(db_name, doc_id):
    message = delete_file(db_name, doc_id)
    return message


def upload_file():
    pass


def download_file():
    pass
