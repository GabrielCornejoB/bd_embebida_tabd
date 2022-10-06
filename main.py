import eel
import os
import json
import sqlite3 as sql

eel.init(os.path.dirname(os.path.realpath(__file__)) + "\\web")

eel.start("index.html")