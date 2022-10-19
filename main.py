import eel
import os
import json
import sqlite3 as sql
import sys

# eel.init(os.path.dirname(os.path.realpath(__file__)) + "\\web")
eel.init("web")

@eel.expose
def select(table_name):
    if(table_name.isalpha()):
        conn = sql.connect("pescasDB.sqlite")
        cursor = conn.cursor()
        rows = cursor.execute("SELECT * FROM " + table_name).fetchall()
        conn.close()
        if(len(rows) > 0):
            return json.dumps(rows, ensure_ascii=False).encode('utf-8').decode()
        else:
            return "[err] Query returned 0 rows"
    else:
        return "[err] Table name must be alphabetic only"

eel.start("index.html", size=(1080, 720))