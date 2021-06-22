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
            conn.execute(create_status)

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

    def get_accounts(self, id_user_active, flag_search = 0):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            if flag_search == 1:
                accounts = cur.execute(f"""SELECT id, login, avatar FROM Main WHERE id <> {id_user_active} """).fetchall()
                return accounts
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
            accounts = conn.execute("""SELECT Count(*) FROM Main""").fetchone()
            accounts = accounts[0]  #Потому что кортеж
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
    
    def get_all_followed(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            ids = self.get_id_followed(id)
            all_followed = []
            for i in ids:
                acc = self.get_account_by_Id(i)
                avatar = acc[4]
                name = acc[1]
                id_F = i
                follow = [avatar,name,id_F]
                all_followed.append(follow)
            return all_followed

    def del_followed(self,id_main,id_del):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            deletF = (f'''DELETE FROM Followed WHERE id_onUser = {id_main} AND id_other = {id_del}''')
            cur.execute(deletF)
            conn.commit()


    def get_id_following(self,id):
        with self.get_db_connection() as conn:
            ids = []
            cur = conn.cursor()
            tmp = cur.execute(f"""SELECT id_other FROM Following WHERE id_onUser = {id}""").fetchall()
            conn.commit()
            for i in tmp:
                ids.append(i[0])
            return ids


    def get_all_following(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            ids = self.get_id_following(id)
            all_followed = []
            for i in ids:
                acc = self.get_account_by_Id(i)
                avatar = acc[4]
                name = acc[1]
                id_F = i
                follow = [avatar,name,id_F]
                all_followed.append(follow)
            return all_followed
    
    def del_following(self,id_main,id_del):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            deletF = (f'''DELETE FROM Following WHERE id_onUser = {id_main} AND id_other = {id_del}''')
            cur.execute(deletF)
            conn.commit()
                
    def get_posts_on_acc(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            tmp = cur.execute(f"""SELECT * FROM Post WHERE id_onUser = {id}""").fetchall()
            conn.commit()
            posts = []
            for i,rowp in enumerate(tmp):
                id_post = rowp[0]
                userFromP = self.get_account_by_Id(rowp[4])
                logoP = userFromP[4]
                nameP = userFromP[1] 
                timesP = time.strftime('%d:%m:%Y', time.gmtime(rowp[3]))
                textP = rowp[5]
                likes = cur.execute(f"""SELECT count (*) FROM like WHERE id_post = {id_post} AND status_like = 1""").fetchone()
                post = [id_post,logoP,nameP,timesP,textP,likes[0],[]]
                posts.append(post)
                comments_on_post = cur.execute(f"""SELECT * FROM comment WHERE id_post = {rowp[0]}""").fetchall()
                for j, rowc in enumerate(comments_on_post):
                    userFromCom = self.get_account_by_Id(rowc[1])
                    comment = []
                    logoC = userFromCom[4]
                    nameC = userFromCom[1]
                    timesС = time.strftime('%d:%m:%Y', time.gmtime(rowc[3]))
                    textС = rowc[2]
                    comment = ([logoC,nameC,timesС,textС])
                    posts[i][6].append(comment)
        posts = list(reversed(posts))
        return posts
    def insert_post(self,id,text,id_account):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            acc = self.get_account_by_Id(id)
            id_post = cur.execute(f"""SELECT count (*) FROM Post""").fetchone()
            id_post = id_post[0]+1
            photo_url = None
            id_onUser = id
            times = time.time()
            id_fromUser = id_account
            title = text
            parameters = [id_post,photo_url,id_onUser,times,id_fromUser,title]
            cur.execute(insert_post, parameters)
            conn.commit()

    def delete_post(self,id_post):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            deleteP = (f'''DELETE FROM Post WHERE id_post = {id_post}''')
            deleteC = (f'''DELETE FROM Comment WHERE id_post = {id_post}''')
            cur.execute(deleteP)
            cur.execute(deleteC)
            conn.commit()
    
    def get_settings_user(self, id_u):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            get_set = f"""SELECT * FROM Status WHERE id_user = {id_u}"""
            answer = cur.execute(get_set).fetchone()

            dict = {}
            if answer == None:
                create_c = (f"""INSERT INTO Status (id_user, status_text, year, country) VALUES ({id_u}, 'Нет статуса', 'Нет даты рождения', 'Инопланетянин') """)
                cur.execute(create_c)
                conn.commit
                dict['title'] = 'Нет статуса'
                dict['year'] = 'Нет даты рождения'
                dict['country'] = 'Инопланетянин'
                return dict
            dict['title'] = str(answer[1])
            dict['year'] = str(answer[2])
            dict['country'] = str(answer[3])
            return dict
    
    def update_set(self,status,year,country, id_u):
        with self.get_db_connection() as conn:
            update_c = (f"""UPDATE Status SET status_text = '{status}', year = '{year}', country = '{country}' WHERE id_user = {id_u}""")
            cur = conn.cursor()
            cur.execute(update_c)
            conn.commit
        
    def get_search_result(self, id_user_active, search):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            oper = f"""SELECT id, login, avatar FROM Main WHERE id <> {id_user_active} AND login LIKE '{search}%'"""
            accounts = cur.execute(oper).fetchall()
            if len(accounts) == 0:
                return None
            else:
                return accounts

    def insert_comment(self,id_account,text,id_post):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            acc = self.get_account_by_Id(id_account)

            id_com = cur.execute(f"""SELECT count (*) FROM Comment""").fetchone()
            id_com = id_com[0]+1
            photo_url = None
            id_User = id_account
            times = time.time()
            title = text
            parameters = [id_post,id_User,title,times]
            cur.execute(insert_comment, parameters)
            conn.commit()
    
    def like_com(self, id_from,id_post):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            like_status =cur.execute(f'''SELECT status_like FROM Like WHERE id_post = {id_post} AND id_from = {id_from}''').fetchone()
            print(like_status)
            if like_status == None:
                like_status = 1
                like_update = f"""INSERT INTO Like (id_post, id_from, status_like) VALUES ({id_post}, {id_from}, {like_status})"""
                cur.execute(like_update)
            elif like_status[0] == 1:
                like_status = 0
                like_update = (f"""UPDATE Like SET status_like = '{like_status}' WHERE id_post = {id_post} AND id_from = {id_from}""")
                cur.execute(like_update)
            else:
                like_status = 1
                like_update = (f"""UPDATE Like SET status_like = '{like_status}' WHERE id_post = {id_post} AND id_from = {id_from}""")
                cur.execute(like_update)
            conn.commit()

    def get_count_followed_and_following(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            followed = cur.execute(f"""SELECT count (*) FROM Followed WHERE id_onUser = {id}""").fetchone()
            following = cur.execute(f"""SELECT count (*) FROM Following WHERE id_onUser = {id}""").fetchone()
            follow = [followed[0],following[0]]
        return follow