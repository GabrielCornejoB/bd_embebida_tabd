import eel
import os
import json
import sqlite3 as sql

eel.init(os.path.dirname(os.path.realpath(__file__)) + "\\web")

@eel.expose
def select(table_name):
    conn = sql.connect("pescasDB.sqlite")
    cursor = conn.cursor()

    query = cursor.execute("SELECT * FROM " + table_name)

    conn.close()


eel.start("index.html")