import eel
import os
import json
import sqlite3 as sql
import sys

valid_tables = ["cuencas", "metodos", "pescas", "v_pescas_detalle"]
db = "pescasDB.sqlite"

# eel.init(os.path.dirname(os.path.realpath(__file__)) + "\\web")
eel.init("web")

def check_args(args):
    if (type(args) is list) and len(args) > 0:
        for a in args:
            if (not a or (not type(a) is str) or (a.isspace())):
                return False
    return True

def check_existence(val, table, column):
    conn = sql.connect(db)
    cursor = conn.cursor()
    query = "SELECT * FROM " + table + " WHERE " + column + "=(?)"
    rows = cursor.execute(query, [val]).fetchall()
    if(len(rows) > 0):
        return True
    else:
        return False

def jsonize(text):
    return json.dumps(text, ensure_ascii=False).encode('utf-8').decode()

@eel.expose
def select(table_name):
    try:
        table_name = table_name.lower()
        if not table_name in valid_tables:
            return jsonize("[ERROR] Invalid table name!")
        conn = sql.connect(db)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM " + table_name).fetchall()

        if len(rows) == 0:
            return jsonize("[ERROR] Table has 0 entrys :(")

        conn.close()
    except Exception as e:
        return jsonize("[ERROR] " + str(e))
    else:
        return jsonize(rows)

@eel.expose
def create(table_name, args):
    try:
        table_name = table_name.lower()
        query_end = ""

        if not table_name in valid_tables:
            return jsonize("[ERROR] Invalid table name!")
        if not check_args(args):
            return jsonize("[ERROR] Invalid arg(s)!")
        
        if table_name == "cuencas" or table_name == "metodos":
            if len(args) != 1:
                return jsonize("[ERROR] Create on table \"" + table_name + "\" needs exactly 1 argument!")
            else:
                query_end = " (cuenca) VALUES (?)" if table_name=="cuencas" else " (metodo) VALUES (?)"

        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca]
            if len(args) != 4:
                return jsonize("[ERROR] Create on table \"pescas\" needs exactly 4 arguments!")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                except:
                    return jsonize("[ERROR] Args have invalid types")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    return jsonize("[ERROR] Arg #1 doesn't exist in cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    return jsonize("[ERROR] Arg #2 doesn't exist in metodos")
                query_end = " (id_cuenca, id_metodo, fecha_pesca, peso_total_pesca) VALUES (?, ?, ?, ?)"
        
        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "INSERT INTO " + table_name + query_end
        cursor.execute(query, args)
        conn.commit()

        conn.close()
    except Exception as e:
        return jsonize("[ERROR] " + str(e))
    else:
        return jsonize("[MSG] Entry created succesfully! :)")

@eel.expose
def update(table_name, args):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        query_end = ""

        if not table_name in valid_tables:
            return jsonize("[ERROR] Invalid table name!")
        if not check_args(args):
            return jsonize("[ERROR] Invalid arg(s)!")
        if not check_existence(args[-1], table_name, id_name):
            return jsonize("[ERROR] Invalid Id!")

        if table_name == "cuencas" or table_name == "metodos":
            # [0:cuenca, 1:id_cuenca] or [0:metodo, 1:id_metodo]
            if len(args) != 2:
                return jsonize("[ERROR] Update on \"" + table_name + "\" needs exactly 2 arguments!")
            else:
                query_end = "cuenca=(?) WHERE id_cuenca=(?)" if table_name=="cuencas" else "metodo=(?) WHERE id_metodo=(?)"
        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca, 4:id_pesca]
            if len(args) != 5:
                return jsonize("[ERROR] Update on \"pescas\" needs exactly 5 arguments!")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                    args[4] = int(args[4])
                except:
                    return jsonize("[ERROR] Args have invalid types!")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    return jsonize("[ERROR] Arg #1 doesn't exist in cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    return jsonize("[ERROR] Arg #2 doesn't exist in metodos")
                query_end = "id_cuenca=(?), id_metodo=(?), fecha_pesca=(?), peso_total_pesca=(?) WHERE id_pesca=(?)"
            
        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "UPDATE " + table_name + " SET " + query_end
        cursor.execute(query, args)
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonize('[ERROR]:' + e)
    else:
        return jsonize("[MSG] Entry updated succesfully!")

@eel.expose
def delete(table_name, arg):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        if not table_name in valid_tables:
            return jsonize("[ERROR] Invalid table name!")
        if not check_args([arg]):
            return jsonize("[ERROR] Invalid arg!")
        if not check_existence(arg, table_name, id_name):
            return jsonize("[ERROR] Invalid Id!")
        if (table_name == "cuencas") and check_existence(arg, "pescas", "id_cuenca"):
            return jsonize("[ERROR] Cuenca #" + arg + " is being used in table pescas!")
        if (table_name == "metodos") and check_existence(arg, "pescas", "id_metodo"):
            return jsonize("[ERROR] Metodo #" + arg + " is being used in table pescas!")

        conn = sql.connect(db)
        cursor = conn.cursor()
        
        query = "DELETE FROM " + table_name + " WHERE " + id_name + "=(?)"
        cursor.execute(query, [arg])
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonize("[ERROR] " + e)
    else:
        return jsonize("[MSG] Entry deleted succesfully!")

eel.start("index.html", cmdline_args=['--start-fullscreen'])