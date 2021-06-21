import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
import time
con = sqlite3.connect("db/sota.db")
cur = con.cursor()
id = 2
tmp = cur.execute(f"""SELECT count (*) FROM Post WHERE id_onUser = {id}""").fetchone()
con.commit()

a= [[1,2,3,[2,3,4]],[1,2,3,[3,4,5]]]
b = []
for i in range(len(a)-1,-1,-1):
    b.append(a[i])
print(b)

a = list(reversed(a))
print(a)