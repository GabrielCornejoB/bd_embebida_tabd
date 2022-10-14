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
