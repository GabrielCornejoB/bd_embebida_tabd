import eel
import os
import json
import sqlite3 as sql
import sys
from datetime import datetime

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
            return jsonize("[ERR]Nombre de tabla no valido")
        conn = sql.connect(db)
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM " + table_name).fetchall()

        if len(rows) == 0:
            return jsonize("[ERR]La tabla tiene 0 registros :(")

        conn.close()
    except Exception as e:
        return jsonize("[ERR]" + str(e))
    else:
        return jsonize(rows)

@eel.expose
def create(table_name, args):
    try:
        table_name = table_name.lower()
        query_end = ""

        if not table_name in valid_tables:
            return jsonize("[ERR]Nombre de tabla no valido")
        if not check_args(args):
            return jsonize("[ERR]Argumentos vacíos o nulos")
        
        if table_name == "cuencas" or table_name == "metodos":
            if len(args) != 1:
                return jsonize("[ERR]La operación CREATE en la tabla \"" + table_name + "\" requiere exactamente de 1 argumento")
            else:
                query_end = " (cuenca) VALUES (?)" if table_name=="cuencas" else " (metodo) VALUES (?)"

        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca]
            if len(args) != 4:
                return jsonize("[ERR]La operación CREATE en la tabla \"pescas\" requiere exactamente de 4 argumentos")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                except:
                    return jsonize("[ERR]Los argumentos son de tipo no valido")
                if float(args[3]) <= float(0):
                    return jsonize("[ERR]El peso de la pesca no puede cero 0 o negativo")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    return jsonize("[ERR]El argumento 1 no existe en la tabla Cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    return jsonize("[ERR]El argumento 2 no existe en la tabla Métodos")
                query_end = " (id_cuenca, id_metodo, fecha_pesca, peso_total_pesca) VALUES (?, ?, ?, ?)"
        
        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "INSERT INTO " + table_name + query_end
        cursor.execute(query, args)
        conn.commit()

        conn.close()
    except Exception as e:
        return jsonize("[ERR] " + str(e))
    else:
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tCREATE on " + table_name + ", args:" + str(args) + "<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")

@eel.expose
def update(table_name, args):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        query_end = ""

        if not table_name in valid_tables:
            return jsonize("[ERR]Nombre de tabla no valido")
        if not check_args(args):
            return jsonize("[ERR]Argumentos vacíos o nulos")
        if not check_existence(args[-1], table_name, id_name):
            return jsonize("[ERR]Id a modificar no valido")

        if table_name == "cuencas" or table_name == "metodos":
            # [0:cuenca, 1:id_cuenca] or [0:metodo, 1:id_metodo]
            if len(args) != 2:
                return jsonize("[ERR]La operación UPDATE en la tabla \"" + table_name + "\" requiere exactamente de 2 argumentos")
            else:
                query_end = "cuenca=(?) WHERE id_cuenca=(?)" if table_name=="cuencas" else "metodo=(?) WHERE id_metodo=(?)"
        if table_name == "pescas":
            # [0:id_cuenca, 1:id_metodo, 2:fecha, 3:peso_total_pesca, 4:id_pesca]
            if len(args) != 5:
                return jsonize("[ERR]La operación UPDATE en la tabla \"pescas\" requiere exactamente de 5 argumentos")
            else:
                try:
                    args[0] = int(args[0])
                    args[1] = int(args[1])
                    args[3] = float(args[3])
                    args[4] = int(args[4])
                except:
                    return jsonize("[ERR]Los argumentos son de tipo no valido")
                if float(args[3]) <= float(0):
                    return jsonize("[ERR]El peso de la pesca no puede cero 0 o negativo")
                if not check_existence(args[0], "cuencas", "id_cuenca"):
                    return jsonize("[ERR]El argumento 1 no existe en la tabla Cuencas")
                if not check_existence(args[1], "metodos", "id_metodo"):
                    return jsonize("[ERR]El argumento 2 no existe en la tabla Métodos")
                query_end = "id_cuenca=(?), id_metodo=(?), fecha_pesca=(?), peso_total_pesca=(?) WHERE id_pesca=(?)"
            
        conn = sql.connect(db)
        cursor = conn.cursor()
        query = "UPDATE " + table_name + " SET " + query_end
        cursor.execute(query, args)
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonize('[ERR]' + e)
    else:
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tUPDATE on " + table_name + ", id: " + str(args[-1]) + ", args: " + str(args) + "<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")

@eel.expose
def delete(table_name, arg):
    try:
        table_name = table_name.lower()
        id_name = "id_" + table_name[:-1]
        if not table_name in valid_tables:
            return jsonize("[ERR]Nombre de tabla no valido")
        if not check_args([arg]):
            return jsonize("[ERR]Argumento vacío o nulo")
        if not check_existence(arg, table_name, id_name):
            return jsonize("[ERR]Id a eliminar no valido")
        if (table_name == "cuencas") and check_existence(arg, "pescas", "id_cuenca"):
            return jsonize("[ERR]La Cuenca #" + arg + " está siendo usada en la tabla Pescas")
        if (table_name == "metodos") and check_existence(arg, "pescas", "id_metodo"):
            return jsonize("[ERR]El Metodo #" + arg + " está siendo usado en la tabla Pescas")

        conn = sql.connect(db)
        cursor = conn.cursor()
        
        query = "DELETE FROM " + table_name + " WHERE " + id_name + "=(?)"
        cursor.execute(query, [arg])
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonize("[ERR]" + e)
    else:
        with open("logs.txt", 'a', encoding='utf-8') as logs:
            logs.write("[" + str(datetime.now())[0:16] + "]\tDELETE on " + table_name + ", (id: " + str(arg) + ")<br>\n")
        return jsonize("[MSG]Operación realizada con exito :)")

@eel.expose
def get_logs():
    logs =  open("logs.txt", 'r', encoding='utf-8')
    data = logs.read()
    logs.close()
    return jsonize(data)

eel.start("index.html", cmdline_args=['--start-fullscreen'])