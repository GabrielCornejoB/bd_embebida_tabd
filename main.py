import eel
import os
import json
import sqlite3 as sql
import sys

valid_tables = ["cuencas", "metodos", "pescas"]
db = "pescasDB.sqlite"

# eel.init(os.path.dirname(os.path.realpath(__file__)) + "\\web")
eel.init("web")

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



eel.start("index.html", size=(1080, 720))