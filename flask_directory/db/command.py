create_main = """CREATE TABLE IF NOT EXISTS Main(
   id INTEGER PRIMARY KEY,
   login TEXT,
   mail TEXT,
   password TEXT,
   avatar BOLD DEFAULT NULL)"""

create_post = """CREATE TABLE IF NOT EXISTS Post(
   id_post INT PRIMARY KEY,
   photo_url TEXT,
   id_onUser INT,
   id_fromUser INT,
   time TIME,
   title TEXT)"""

create_comment = """CREATE TABLE IF NOT EXISTS Comment(
   id_post INT,
   id_User INT,   
   text_c TEXT)"""

create_like = """CREATE TABLE IF NOT EXISTS Like(
   id_post INT,
   id_from INT)"""

create_followed = """CREATE TABLE IF NOT EXISTS Followed(
   id_onUser INT,
   id_other INT)"""

create_following = """CREATE TABLE IF NOT EXISTS Following(
   id_onUser INT,
   id_other INT)"""

create_comment = """CREATE TABLE IF NOT EXISTS Comment(
   id_from INT,
   id_to INT,
   text_c TEXT)"""

insert_account = """INSERT INTO Main (login, mail, password,avatar) VALUES (?, ?, ?,"/static/img/default.png")"""

insert_post = """INSERT INTO post (id_post, photo_url, id_onUser, time, id_fromUser, title) VALUES (?, ?, ?, ?, ?, ?)"""
