from flask import Flask, render_template, redirect, request, jsonify
from datetime import datetime
import sqlite3
import os
from db.database import Database

DATABASE = 'db/sota.db'

app = Flask(__name__)

db = Database(DATABASE)
db.init_db()
accounts = db.get_accounts() #Кол-во всех аккаунтов 
app = Flask(__name__)

flag_enter = False

@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')

@app.route("/fail")
def title_fail():
    return render_template('/title_frame/title_frame_fail.html')

@app.route("/check_enter", methods=['post'])
def check_enter():
    global flag_enter
    if request.form:
        login = request.form.get('login')
        password = request.form.get('password')

        user = db.get_account(login, password)
        if user == None:
            return redirect("/fail")
        else:
            flag_enter = True
            id = db.get_id(login,password)
            return redirect(f'/user_page/{id}') 

@app.route("/forgotten_password")
def for_password():
    return render_template('forgotten_password/forgotten_password.html')

@app.route("/register", methods=['post'])
def register():
    if request.form:
        mail = request.form.get('mail')
        login = request.form.get('login')
        password = request.form.get('password')
        user = {'login': login, 'mail': mail, 'password': password}
        db.insert_account(user)
    return redirect("/")


@app.route('/add')
def posts_add():
    if flag_enter == False:
        return redirect("/")
    else:
        return render_template('register_form/register_form.html')


@app.route("/user_page/<int:id>")
def user_page(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('user_page/user_page.html',account = db.get_account_by_Id(id))


@app.route("/messange/<int:id>")
def for_messanges(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('messange_page/messange_page.html',account = db.get_account_by_Id(id))


@app.route("/followers/<int:id>")
def for_followers(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('my_followers/my_followers.html',account = db.get_account_by_Id(id))


@app.route("/me_following/<int:id>")
def for_following(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('me_following/me_following.html',account = db.get_account_by_Id(id))


@app.route("/news/<int:id>")
def for_news(id):
    if id not in range(1, accounts + 1):
        return "", 404
    else:
        if flag_enter == False:
            return redirect("/")
        else:
            return render_template('news/news.html',account = db.get_account_by_Id(id))


@app.route("/404_erros")
def for_404_error():
    return render_template('404_error/404_error.html')