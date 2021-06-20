import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
con = sqlite3.connect("db/sota.db")
cur = con.cursor()
mail = cur.execute(f"""SELECT mail FROM Main WHERE mail = 'vladik01.04.2002@mail.ru'""").fetchone()

print(mail[0])