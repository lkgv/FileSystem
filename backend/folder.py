from backend.sql import *
db_name = "../test.db"


class Folder:
    def __init__(self, folder_id, folder_name):
        self.folder_id = folder_id
        self.folder_name = folder_name
        if folder_id != 1:
            father_folder = get_father_folder(db_name, folder_id)
        else:
            father_folder = {"folder_id": 0, "folder_name": "fuck"}
        self.father_id = father_folder["folder_id"]
        self.father_name = father_folder["folder_name"]

    def get_children(self):
        print('flag')
        children = find_children(db_name, self.folder_id)
        result = []
        print("1")
        if children["error"] == "":
            print("2")
            folders = children["folders"]
            documents = children["documents"]
            print("folders:", folders)
            print("documents:", documents)
        else:
            print(children["error"], 2)
            return "error"
        for folder in folders:
            tmp = {"is_folder": True, "id": folder["folder_id"], "name": folder["folder_name"], "size": "", "date": ""}
            result.append(tmp)
        print("3")
        for document in documents:
            tmp = {"is_folder": False, "id": document["doc_id"], "name": document["doc_name"], "size": document["doc_size"],
                   "date": document["doc_last_change_date"]}
            result.append(tmp)
        return result

    @staticmethod
    def go_into_child(child_id, child_name):
        child = Folder(child_id, child_name)
        return child

    def go_back_father(self):
        if self.father_id != 0:
            print(self.father_name, self.father_id)
            return Folder(self.father_id, self.father_name)
        else:
            return "no father"

    def add_file(self):
        pass

    def add_folder(self, folder_name):
        add_folder(db_name, self.folder_id, folder_name)

    @staticmethod
    def change_folder_name(folder_id, new_name):
        rename_folder(db_name, folder_id, new_name)

    @staticmethod
    def change_file_name(file_id, new_name):
        print(rename_file(db_name, file_id, new_name))

    def paste(self, item):
        if item["is_folder"]:
            relink_folder(db_name, self.folder_id, item["id"])
        else:
            relink_document(db_name, self.folder_id, item["id"])
        print(db_name, self.folder_id, item["id"])

    @staticmethod
    def delete(item):
        if item["is_folder"]:
            delete_folder(db_name, item["id"])
        else:
            delete_file(db_name, item["id"])
