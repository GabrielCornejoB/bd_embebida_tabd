import sqlite3 as sql

def select(table_name):
    conn = sql.connect("pescasDB.sqlite")
    cursor = conn.cursor()

    query = cursor.execute("SELECT * FROM " + table_name)
    print(query)

    conn.close()
