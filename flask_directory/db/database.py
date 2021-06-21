from db.command import * 
import os
import sqlite3
from PIL import Image 
from werkzeug.security import check_password_hash
import time
#КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ 
#КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ  
#КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ КОМЕНТЫ ОСТАВЛЯЙ
class Database:
    
    def __init__(self, database_name):
        self.database_name = database_name

    def get_db_connection(self):
        conn = sqlite3.connect(self.database_name)
        conn.row_factory = sqlite3.Row
        return conn

    def create_db(self):
        with self.get_db_connection() as conn:
            conn.execute(create_main)
            conn.execute(create_post)
            conn.execute(create_comment)
            conn.execute(create_like)
            conn.execute(create_followed)
            conn.execute(create_following)
            conn.execute(create_following)

    def init_db(self):
        if not os.path.exists(self.database_name):
            self.create_db()
            with self.get_db_connection() as conn:
                conn.commit()
    
    def insert_account(self, acc):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            parameters = [acc['login'], acc['mail'], acc['password']]
            cur.execute(insert_account, parameters)
            conn.commit()
        
    def create_img_folder(self,id):
        path = "static\img"
        projectame = str(id)
        fullpath = os.path.join(path,projectame)
        print(fullpath)
        os.mkdir(fullpath)
        seek_f = open(f"{fullpath}/.gitkeep","w") # чтобы в гит отправлялись пустые папки

    def check_mail(self,mail):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            mail_checked = cur.execute(f"""SELECT mail FROM Main WHERE mail = '{mail}'""").fetchone()
            if mail_checked == None:
                return False
        return True

    def get_account(self, login, password):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            account = cur.execute(f"""SELECT id FROM Main WHERE (login = '{login}') and (password = '{password}')""").fetchone()
        return account

    def get_accounts(self):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            accounts = cur.execute(f"""SELECT * FROM Main""").fetchall()
        return accounts

    def get_account_by_Id(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            account = conn.execute(f"""SELECT * FROM Main WHERE id = {id}""").fetchone()
        return account

    def get_accounts_count(self): # Считает кол-во аккаунтов
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            accounts = conn.execute("""SELECT Count(*) FROM Main""").fetchall()
            accounts = accounts[0][0]  #Костыль
        return accounts

    def get_id(self,login):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            id = cur.execute(f"""SELECT id FROM Main WHERE (login = '{login}')""").fetchone()
            id = id[0]
        return id

    def check_avatar(self,id,filename):
        im = Image.open(f"static/img/{id}/{filename}")
        (width, height) = im.size
        print(width,height)
        if width > 500 or height >500:
            return False
        return True

    def change_avatar(self,id,filename):
        with self.get_db_connection() as conn:
            
            cur = conn.cursor()
            new = cur.execute(f"""UPDATE main SET avatar = "/static/img/{id}/{filename}" WHERE id = {id}""")
            conn.commit()
        return 

    def check_enter_acc(self,login,password):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            acc = cur.execute(f"""SELECT * FROM main WHERE login = '{login}'""").fetchone()
            conn.commit()
            if login == acc[1] and check_password_hash(acc[3],password) == True:
                return True
            else:
                return False


    def check_account(self,parametrs):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            mail,login,password,password2 = parametrs[0],parametrs[1],parametrs[2],parametrs[3],
            errors = ["display: Block;","display: Block;","display: Block;","display: Block;","display: Block;","display: Block;"]
            if "@" in mail:
                errors[0] = "display: none;"
                MAIL = cur.execute(f"""SELECT mail FROM Main WHERE (mail = '{mail}')""").fetchone()
                if MAIL != mail:
                    errors[1] = "display: None;"
            if len(login)>=6 and len(login) <= 15:
                errors[2] = "display: none;"
                LOGIN = cur.execute(f"""SELECT login FROM Main WHERE (login = '{login}')""").fetchone()
                conn.commit()
                if LOGIN != login:
                    errors[3] = "display: None;"
            if len(password) >= 6:
                errors[4] = "display: none;"
            if password == password2:
                errors[5] = "display: none;"
            return errors

    def get_id_followed(self,id):
        with self.get_db_connection() as conn:
            ids = []
            cur = conn.cursor()
            tmp = cur.execute(f"""SELECT id_other FROM Followed WHERE id_onUser = {id}""").fetchall()
            conn.commit()
            for i in tmp:
                ids.append(i[0])
            return ids

    def get_posts_on_acc(self,id):
        with self.get_db_connection() as conn:
            posts = []
            comments = []
            cur = conn.cursor()
            tmp = cur.execute(f"""SELECT * FROM Post WHERE id_onUser = {id}""").fetchall()
            conn.commit()
            for i, row in enumerate(tmp):
                post_id = row[0]
                userFrom = self.get_account_by_Id(row[4])
                logo = userFrom[4]
                name = userFrom[1] 
                times = time.strftime('%d:%m:%y', time.gmtime(row[3]))
                text = row[5]
                posts.append([logo,name,times,text,post_id])
                # comments_on_post = cur.execute(f"""SELECT * FROM comment WHERE id_post = {post_id}""").fetchall()
                # for com in enumerate(comments_on_post):
                #     comments.append([])
                #     userFrom = self.get_account_by_Id(row[1])
                #     logo = userFrom[4]
                #     name = userFrom[1] 
                #     times = time.strftime('%d:%m:%y', time.gmtime(row[3]))
                #     text = row[2]
                #     comments.append([logo,name,times,text])

            return posts
    def get_comments(self,id_post):
        with self.get_db_connection() as conn:
            comments = []
            cur = conn.cursor()
            tmp = cur.execute(f"""SELECT * FROM comment WHERE id_post = {id_post}""").fetchall()
            conn.commit()
            for row in tmp:
                userFrom = self.get_account_by_Id(row[1])
                logo = userFrom[4]
                name = userFrom[1] 
                times = time.strftime('%d:%m:%y', time.gmtime(row[3]))
                text = row[2]
                comments.append([logo,name,times,text])
            return comments