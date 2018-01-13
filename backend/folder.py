from backend.sql import *
db_name = "test.db"


class Folder:
    def __init__(self, folder_id, folder_name):
        self.folder_id = folder_id
        self.folder_name = folder_name
        father_folder = get_father_folder(db_name, folder_id)
        self.father_id = father_folder["folder_id"]
        self.father_name = father_folder["folder_name"]

    def get_children(self):
        children = find_children(db_name, self.folder_id)
        result = []
        if children["error"] == 0:
            folders = children["folders"]
            documents = children["documents"]
        else:
            return "error"
        for folder in folders:
            tmp = {"is_folder": True, "id": folder[0], "name": folder[1], "size": "", "date": ""}
            result.append(tmp)
        for document in documents:
            tmp = {"is_folder": False, "id": document[0], "name": document[1], "size": document[2],
                   "date": document[3]}
            result.append(tmp)
        return result

    @staticmethod
    def go_into_child(self, child_id, child_name):
        child = Folder(child_id, child_name, self.folder_id, self.folder_name)
        return child

    def go_back_father(self):
        if self.father_id != 0:
            return Folder(self.father_id, self.father_name)
        else:
            return "no father"

    def add_file(self):
        pass

    def add_folder(self, folder_name):
        add_folder(db_name, self.folder_id, folder_name)

    def change_name(self, new_name):
        rename_folder(db_name, self.folder_id, new_name)

    @staticmethod
    def change_file_name(self, file_id, new_name):
        rename_file(db_name, file_id, new_name)

    @staticmethod
    def paste(self, item):
        if item["is_folder"]:
            relink_folder(db_name, self.folder_id, item["id"])
        else:
            relink_document(db_name, self.folder_id, item["id"])

    @staticmethod
    def delete(self, item):
        if item["is_folder"]:
            delete_folder(db_name, item["id"])
        else:
            delete_file(db_name, item["id"])
