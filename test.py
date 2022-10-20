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

def check_fk(val, table):
    conn = sql.connect(db)
    cursor = conn.cursor()
    id_name = "id_" + table[:-1]
    query = "SELECT * FROM " + table + " WHERE " + id_name + "=(?)"
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
        
        if (table_name == "cuencas" or table_name == "metodos"):
            if len(args) != 1:
                raise Exception("Table \"" + table_name + "\" needs exactly 1 argument!")
            else:
                query_end = " (cuenca) VALUES (?)" if table_name=="cuencas" else " (metodo) VALUES (?)"

        if (table_name == "pescas"):
            if len(args) != 4:
                raise Exception("Table \"pescas\" needs exactly 4 arguments!")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                except:
                    raise Exception("Args have invalid types")
                if not check_fk(args[0], "cuencas"):
                    raise Exception("Arg #1 doesn't exist in cuencas")
                if not check_fk(args[1], "metodos"):
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

