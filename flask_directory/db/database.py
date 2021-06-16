from db.command import * 
import os.path
import sqlite3

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
    
    def insert_post(self, acc):
        with self.get_db_connection() as conn:
            parameters = [acc['login'], acc['mail'], acc['password']]
            cur = conn.cursor()
            cur.execute(insert_acc, parameters)
            lastrowid = cur.lastrowid
            conn.commit()
        return lastrowid