import sqlite3 as sql
import json

def select (table_name):
    if (table_name.isalpha()):
        conn = sql.connect("pescasDB.sqlite")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM " + table_name).fetchall()
        conn.close()
        if (len(rows) > 0):
            return json.dumps(rows, ensure_ascii=False).encode('utf-8').decode()
    else:
        return "[err] Input was not alphabetic only"

def create(table_name, args):
    valid_tables = ["cuencas", "metodos", "pescas"]
    if (table_name.isalpha() and (table_name in valid_tables)):
        conn = sql.connect("pescasDB.sqlite")
        cursor = conn.cursor()
        query = "INSERT INTO"

        if (table_name == valid_tables[0]):
            query = query + " cuencas (cuenca)"
        elif (table_name == valid_tables[1]):
            query = query + " metodos (metodo)"
        elif (table_name == valid_tables[2]):
            print("no implementado para tabla pescas todavía")

        if(len(args) == 1 and args[0] and (not args[0].isspace())):
            query = query + " VALUES (?)"
            cursor.execute(query, args)
        elif(len(args) == 2):
            print('no implementado para tabla pescas todavía')
        else:
            conn.close()
            return "[err] Invalid arguments"

        conn.commit()
        conn.close()
    else:
        return "[err] Table name not valid"


            

print(create("metodos", ["Abrelatas"]))
print(select("metodos"))