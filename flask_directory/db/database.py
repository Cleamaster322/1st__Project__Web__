from db.command import * 
import os.path
import sqlite3
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
            parameters = [acc['login'], acc['mail'], acc['password']]
            cur = conn.cursor()
            lastrowid = lastrowid = cur.lastrowid
            parameters = [acc['login'], acc['mail'], acc['password']]
            cur.execute(insert_account, parameters)
            conn.commit()
    
    def get_account(self, login, password):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            account = cur.execute(f"""SELECT id FROM Main WHERE (login = '{login}') and (password = '{password}')""").fetchone()
        return account

    def get_account_by_Id(self,id):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            account = conn.execute(f"""SELECT * FROM Main WHERE id = {id}""").fetchone()
        return account

    def get_accounts(self): # Считает кол-во аккаунтов
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            accounts = conn.execute("""SELECT Count(*) FROM Main""").fetchall()
            accounts = accounts[0][0]  #Костыль
        return accounts

    def get_id(self,login,password):
        with self.get_db_connection() as conn:
            cur = conn.cursor()
            id = cur.execute(f"""SELECT id FROM Main WHERE (login = '{login}') and (password = '{password}')""").fetchall()
            id = id[0][0]
        return id