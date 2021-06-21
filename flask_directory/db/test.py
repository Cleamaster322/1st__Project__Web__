import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
import time
con = sqlite3.connect("db/sota.db")
cur = con.cursor()
id = 2
tmp = cur.execute(f"""SELECT * FROM comment WHERE id_post = {2}""").fetchall()

for comm in tmp:
    print(comm)