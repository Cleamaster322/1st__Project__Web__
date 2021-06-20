import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
import time
con = sqlite3.connect("db/sota.db")
cur = con.cursor()
id = 2
account = cur.execute(f"""SELECT * FROM Main WHERE id = {id}""").fetchone()

import time
x = int(1624194398.759357) 
print(time.strftime('%d:%m:%y', time.gmtime(x)))
