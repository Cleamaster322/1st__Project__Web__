import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
con = sqlite3.connect("db/sota.db")
cur = con.cursor()
id = 2
mail = cur.execute(f"""SELECT * FROM Post WHERE id_onUser = {id}""").fetchall()

print(mail[1][3])