import sqlite3
import datetime


def setup_sql(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.executescript("""
            create table Folders(
            folder_id integer primary key autoincrement,
            folder_name varchar(20)
            );

            create table Documents(
            doc_id integer primary key autoincrement,
            doc_name varchar(100),
            doc_hash varchar(100),
            doc_size real,
            doc_last_change_date date
            );

            create table Packages(
            package_id integer primary key autoincrement,
            package_hash varchar(100)
            );

            create table Servers(
            server_id integer primary key autoincrement,
            server_ip varchar(20),
            server_name text
            );

            create table TreePaths(
            father int not null,
            child int not null,
            primary key(father, child),
            foreign key (father) references Folders(folder_id),
            foreign key (child) references Folders(folder_id)
            );

            create table FoldDocs(
            folder_id int not null,
            doc_id int not null,
            primary key (folder_id, doc_id),
            foreign key (folder_id) references Folders(folder_id),
            foreign key (doc_id) references Documents(doc_id)
            );

            create table DocPacks(
            doc_id int not null,
            package_id int not null,
            part int not null,
            primary key (doc_id, package_id, part),
            foreign key (doc_id) references Documents(doc_id),
            foreign key (package_id) references Packages(package_id)
            );

            create table PackSers(
            package_id int not null,
            server_id int not null,
            primary key (server_id, package_id),
            foreign key (package_id) references Packages(package_id),
            foreign key (server_id) references Servers(server_id)
            );
        """)
        cur.execute("insert into Folders(folder_name) values (?)", ("root", ))
        con.commit()
        cur.close()
        con.close()
        return "create table success"
    except sqlite3.Error as e:
        cur.close()
        con.close()
        return "error " + e.args[0]


def add_folder(db_name, father_id, child_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("select * from Folders where folder_id = (?)", (father_id,))
    father = cur.fetchone()
    if father is None:
        print("there is not folder ", father_id)
        return "add folder error"
    else:
        cur.execute("insert into Folders(folder_name) values (?)", (child_name,))
        cur.execute("select last_insert_rowid()")
        child_id = cur.fetchone()[0]
        cur.execute("insert into TreePaths values (?, ?)", (father_id, child_id))
        con.commit()
        cur.close()
        con.close()
        return "add folder success"


def add_file(db_name, folder_id, doc_name, doc_hash, doc_size):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("select * from Folders where folder_id = (?)", (folder_id,))
    folder = cur.fetchone()
    if folder is None:
        print("there is not folder ", folder)
        return "add file error"
    else:
        cur.execute("insert into Documents(doc_name, doc_hash, doc_size, doc_last_change_date) values(?, ?, ?, ?)",
                    (doc_name, doc_hash, doc_size, datetime.date.today()))
        cur.execute("select last_insert_rowid()")
        doc_id = cur.fetchone()[0]
        cur.execute("insert into FoldDocs(folder_id, doc_id) values (?, ?)", (folder_id, doc_id))
        con.commit()
        cur.close()
        con.close()
        return "add file success"


def add_package(db_name, doc_id, package_hash, part):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("select * from Packages where package_hash = (?)", (package_hash,))
        package = cur.fetchall()
        if package.__len__() == 0:
            cur.execute("insert into Packages(package_hash) values (?)", (package_hash,))
            cur.execute("select last_insert_rowid()")
            package_id = cur.fetchone()[0]
        else:
            package_id = package[0][0]
        cur.execute("insert into DocPacks(doc_id, package_id, part) values (?, ?, ?)", (doc_id, package_id, part))
        con.commit()
        cur.close()
        con.close()
    except sqlite3.Error as e:
        cur.close()
        con.close()
        return e.args[0]
    return "add package success"


def delete_folder(db_name, folder_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("select * from Folders where folder_id = (?)", (folder_id,))
    folder = cur.fetchone()
    if folder is None:
        return "there is not this folder"
    else:
        folder = folder[0]
        cur.execute("delete from TreePaths where child = (?)", (folder_id,))
        con.commit()
        cur.close()
        con.close()
        return "delete folder success"


def delete_file(db_name, doc_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("select * from Documents where doc_id = (?)", (doc_id,))
    doc = cur.fetchone()
    if doc is None:
        return "there id not this document"
    else:
        doc = doc[0]
        cur.execute("delete from FoldDocs where doc_id = (?)", (doc_id,))
        con.commit()
        cur.close()
        con.close()
        return "delete document success"


def rename_folder(db_name, folder_id, folder_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("update Folders set folder_name = (?) where folder_id = (?)", (folder_name, folder_id))
        con.commit()
        cur.close()
        con.close()
        return "rename folder success"
    except Exception as e:
        cur.close()
        con.close()
        return "rename folder error " + str(e)


def rename_file(db_name, doc_id, doc_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    try:
        cur.execute("update Documents set doc_name = (?) where doc_id = (?)", (doc_name, doc_id))
        con.commit()
        cur.close()
        con.close()
        return "rename document success"
    except Exception as e:
        cur.close()
        con.close()
        return "rename document error " + str(e)


def find_children(db_name, folder_id):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    result = {"folders": [], "documents": [], "error": ""}
    try:
        cur.execute("select f.* from Folders as f join TreePaths as t on f.folder_id = t.child where t.father = (?)", (folder_id,))
        child_folder = cur.fetchall()
        if child_folder is not None:
            tmp = []
            for child in child_folder:
                tamp = {
                    "folder_id": child[0],
                    "folder_name": child[1]
                }
                tmp.append(tamp)
            result["folders"] = tmp
        cur.execute("select d.* from Documents as d join FoldDocs as fd on d.doc_id = fd.doc_id where fd.folder_id = (?)", (folder_id,))
        child_doc = cur.fetchall()
        if child_doc.__len__() != 0:
            tmp = []
            for child in child_folder:
                tamp = {
                    "doc_id": child[0],
                    "doc_name": child[1],
                    "doc_size": child[3],
                    "doc_last_change_date": child[4]
                }
                tmp.append(tamp)
            result["documents"] = tmp
        con.commit()
        cur.close()
        con.close()
    except Exception as e:
        result["error"] = str(e)
    return result
