import sqlite3 as sql
import json
import sys

valid_tables = ["cuencas", "metodos", "pescas"]
db = "pescasDB.sqlite"

def check_args(args):
    if (type(args) is list) and len(args) > 0:
        for a in args:
            if (a and (type(a) is str) and (not a.isspace())):
                return True
    return False

def check_existence(val, table, column):
    conn = sql.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM " + table + " WHERE " + column + "=(?)"
    rows = cursor.execute(query, [val]).fetchall()
    if(len(rows) > 0):
        return True
    else:
        return False

def select (table_name):
    try:
        table_name = table_name.lower()
        if not table_name in valid_tables:
            raise Exception("Invalid table name!")

        conn = sql.connect(db)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM " + table_name).fetchall()

        if len(rows) == 0:
            raise Exception("Table has 0 entrys :(")

        conn.close()
    except Exception as e:
        print("ERROR:",e)
    else:
        print(json.dumps(rows, ensure_ascii=False).encode('utf-8').decode())

def create(table_name, args):
    try:
        table_name = table_name.lower()
        query_end = ""

        if not table_name in valid_tables:
            raise Exception("Invalid table name!")
        if not check_args(args):
            raise Exception("Invalid arg(s)!")
        
        if table_name == "cuencas" or table_name == "metodos":
            if len(args) != 1:
                raise Exception("Create on table \"" + table_name + "\" needs exactly 1 argument!")
            else:
                query_end = " (cuenca) VALUES (?)" if table_name=="cuencas" else " (metodo) VALUES (?)"

        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca]
            if len(args) != 4:
                raise Exception("Create on table \"pescas\" needs exactly 4 arguments!")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                except:
                    raise Exception("Args have invalid types")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    raise Exception("Arg #1 doesn't exist in cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    raise Exception("Arg #2 doesn't exist in metodos")
                query_end = " (id_cuenca, id_metodo, fecha_pesca, peso_total_pesca) VALUES (?, ?, ?, ?)"
        
        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "INSERT INTO " + table_name + query_end
        cursor.execute(query, args)
        conn.commit()

        conn.close()
    except Exception as e:
        print("ERROR:",e)
    else:
        print("Entry created succesfully!")

def update(table_name, args):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        query_end = ""

        if not table_name in valid_tables:
            raise Exception("Invalid table name!")
        if not check_args(args):
            raise Exception("Invalid arg(s)!")
        if not check_existence(args[-1], table_name, id_name):
            raise Exception("Invalid Id!")

        if table_name == "cuencas" or table_name == "metodos":
            # [0:cuenca, 1:id_cuenca] or [0:metodo, 1:id_metodo]
            if len(args) != 2:
                raise Exception("Update on \"" + table_name + "\" needs exactly 2 arguments!")
            else:
                query_end = "cuenca=(?) WHERE id_cuenca=(?)" if table_name=="cuencas" else "metodo=(?) WHERE id_metodo=(?)"
        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca, 4:id_pesca]
            if len(args) != 5:
                raise Exception("Update on \"pescas\" needs exactly 5 arguments!")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                    args[4] = int(args[4])
                except:
                    raise Exception("Args have invalid types!")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    raise Exception("Arg #1 doesn't exist in cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    raise Exception("Arg #2 doesn't exist in metodos")
                query_end = "id_cuenca=(?), id_metodo=(?), fecha_pesca=(?), peso_total_pesca=(?) WHERE id_pesca=(?)"

        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "UPDATE " + table_name + " SET " + query_end
        cursor.execute(query, args)
        conn.commit()
        conn.close()
    except Exception as e:
        print('ERROR:',e)
    else:
        print("Entry updated succesfully!")

def delete(table_name, entry_id):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        if not table_name in valid_tables:
            raise Exception("Invalid table name!")
        if not check_existence(entry_id, table_name, id_name):
            raise Exception("Invalid Id!")
        if (table_name == "cuencas") and check_existence(entry_id, "pescas", "id_cuenca"):
            raise Exception("Cuenca #" + entry_id + " is being used in table pescas!")
        if (table_name == "metodos") and check_existence(entry_id, "pescas", "id_metodo"):
            raise Exception("Metodo #" + entry_id + " is being used in table pescas!")

        conn = sql.connect(db)
        cursor = conn.cursor()
        
        query = "DELETE FROM " + table_name + " WHERE " + id_name + "=(?)"
        cursor.execute(query, [entry_id])
        conn.commit()
        conn.close()
    except Exception as e:
        print("ERROR:",e)
    else:
        print("Entry deleted succesfully!")
