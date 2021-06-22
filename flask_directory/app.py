from flask import Flask, render_template, redirect, request, url_for, send_from_directory,session,flash, make_response
from datetime import datetime
import sqlite3
import os
from flask.helpers import flash
from db.database import Database
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
import smtplib
from email.mime.multipart import MIMEMultipart    
from email.mime.text import MIMEText                
from email.mime.base import MIMEBase
from email import encoders

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

DATABASE = 'db/sota.db'

app = Flask(__name__)
app.secret_key = str(os.urandom(20).hex())
MAX_CONTENT_LENGHT = 1024 * 1024
db = Database(DATABASE)
db.init_db() 
accounts = db.get_accounts_count() #Кол-во всех аккаунтов 

flag_enter = False
id_account = -1

session = {}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET'])  # ГЛАВНАЯ ВХОД
def title():
    global flag_enter
    global id_account
    flag_enter = False
    id_account = -1
    username_id = request.cookies.get('username_id')
    if username_id:
        flag_enter = True
        id_account = int(username_id)
        return redirect(url_for('user_page', id = id_account ))
    return render_template('/title_frame/title_frame.html')


@app.route('/upload_n', methods=['GET', 'POST'])  #ЗАГРУЗКА ФОТО
def upload_file():
    if request.method == 'POST':
        file = request.files['img']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            UPLOAD_FOLDER = f'static/img/{id_account}' #Пришлось сюда перенести мб потом переделаем
            app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            send_from_directory(app.config['UPLOAD_FOLDER'], filename)
            # if db.check_avatar(id_account,filename) == True: # Ограничение на фото 500х500
            #     db.change_avatar(id_account,filename)
            # else:
            #     os.remove(f"static/img/{id_account}/{filename}")
            db.change_avatar(id_account,filename)
            return redirect(f'/user_page/{id_account}')
    else:
        return redirect("/404_erros")
    


@app.route("/check_enter", methods=['post'])  # ПРОВЕРКА АККАУНТА И СОЗДАНИЕ КУКИ
def check_enter():
    global flag_enter
    global id_account
    global session
    if request.form:
        login = request.form.get('login')
        password = request.form.get('password')
        checked = request.form.get('checked')
        if db.check_enter_acc(login,password) == False:
            flash('Неверный логин или пароль')
            return render_template('/title_frame/title_frame.html')
        else:
            session[id_account] = True
            flag_enter = True
            id_account = db.get_id(login)
            if checked == '1':
                resp = make_response(redirect('/'))
                resp.set_cookie('username_id', str(id_account))
                return resp
            else:
                return redirect(url_for('user_page', id = id_account ))

@app.route("/forgotten_password",methods=['post',"get"])  # ВОССТАНОВИТЬ ПАРОЛЬ
def for_password():
    return render_template("forgotten_password/forgotten_password.html")
 


@app.route("/send_pas",methods=['post',"get"])  # ОТПРАВКА ПИСЬМА
def send_pas():
    addr_from = "s.o.t.a.inc@mail.ru"
    password = "bYAJHVFNBRF322"
    addr_to = request.form.get('mail')
    

    msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = "Восстановление пароля"
    if db.check_mail(addr_to) == True:
        msg.attach(MIMEText("123"))
        smtpObj = smtplib.SMTP('smtp.mail.ru', 587)
        smtpObj.starttls()
        smtpObj.login(addr_from,password)
        text = msg.as_string()
        smtpObj.sendmail(addr_from, addr_to, text)
        smtpObj.quit()
        flash("Письмо отправлено")
    else:
        flash("Письмо не отправлено")
    return render_template("forgotten_password/forgotten_password.html")


@app.route("/register", methods=['post'])  # РЕГИСТРАЦИЯ
def register():
    global accounts
    if request.form:
        mail = request.form.get('mail')
        login = request.form.get('login')
        password = request.form.get('password')
        password2 = request.form.get('repeat the password')
        errors = db.check_account([mail,login,password,password2])
        
        for i in errors:
            if i == "display: Block;":
                return post_add_fail(errors)

        user = {'login': login, 'mail': mail, 'password': generate_password_hash(password)}
        db.insert_account(user)
        db.create_img_folder(db.get_id(login))
        accounts +=1
    return redirect("/")


@app.route('/add')  # ДОБАВЛЕНИЕ ПОСТА
def post_add():
    return render_template('register_form/register_form.html')

@app.route('/add_fail',methods = ['GET, POST'])  # ------------------
def post_add_fail(errors):
    return render_template('register_form/register_form_fail.html',errors = errors)


@app.route("/user_page/<int:id>")  # СТРАНЦИЦА ЮЗЕРА
def user_page(id):
    if id not in range(1, accounts + 1) and id != id_account:
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            posts = db.get_posts_on_acc(id)
            lens = len(posts)
            print(lens)
            return render_template('user_page/user_page.html',account = db.get_account_by_Id(id),posts = posts, lens = lens)

@app.route("/add_post/<int:id>", methods=['post'])
def add_post(id):
    account = db.get_account_by_Id(id)
    if request.form:
        text = request.form.get('text_post')
        post = db.insert_post(id,text,id_account)
    return redirect(f"/user_page/{id}")

@app.route("/del_post/<int:id>/<int:id_post>", methods=['post'])
def del_post(id,id_post):
    db.delete_post(id_post)
    return redirect(f"/user_page/{id}")
    

@app.route("/messange/<int:id>")  # СООБЩЕНИЕ
def for_messanges(id):
    if id not in range(1, accounts + 1):
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            return render_template('messange_page/messange_page.html',account = db.get_account_by_Id(id))


@app.route("/followers/<int:id>")  # ПОДПИСЧИКИ
def for_followers(id):
    if id not in range(1, accounts + 1):
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            return render_template('my_followers/my_followers.html',account = db.get_account_by_Id(id))


@app.route("/me_following/<int:id>")  # ТВОИ ПОДПИСКИ
def for_following(id):
    if id not in range(1, accounts + 1):
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            return render_template('me_following/me_following.html',account = db.get_account_by_Id(id))


@app.route("/news/<int:id>")  #  НОВОСТНАЯ ЛЕНТА
def for_news(id):
    if id not in range(1, accounts + 1):
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            return render_template('news/news.html',account = db.get_account_by_Id(id))

@app.route("/find_friends/<int:id>")  #   НАЙТИ ДРУЗЕЙ
def for_find_friends(id):
    if id not in range(1, accounts + 1):
        return redirect("/404_erros")
    else:
        if flag_enter == False or id != id_account:
            return redirect("/")
        else:
            return render_template('search_people_page/search_people_page.html',account = db.get_account_by_Id(id),accounts = db.get_accounts(),id_friends = db.get_id_followed(id))



@app.route("/404_erros")  # ЕЩЕ ОШИБКА БЛ%#$
def for_404_error():
    return render_template('404_error/404_error.html')

@app.route('/logout', methods = ['GET'])   # ВЫХОД
def logout():
    flag_enter = False
    id_account = -1
    resp = make_response(redirect('/'))
    resp.delete_cookie('username_id')
    return resp

@app.route('/setting/<int:id>',methods = ['GET'])
def settings(id):
    return render_template("redacting_profile/redacting_profile.html",account = db.get_account_by_Id(id))



