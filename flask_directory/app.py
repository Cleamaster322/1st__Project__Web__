from flask import Flask, render_template, request, redirect

app = Flask(__name__)


@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')


@app.route("/forgotten_password")
def for_password():
    return render_template('forgotten_password/forgotten_password.html')


@app.route('/add')
def posts_add():
    return render_template('register_form/register_form.html')


@app.route("/register", methods=['user'])
def register():
    if request.form:
        mail = request.form.get('mail')
        login = request.form.get('login')
        password = request.form.get('password')
        user = {'mail': mail, 'login': login, 'password': password}
        post_id = 1
        print(user)
    return redirect("/")


@app.route("/user_page")
def for_database_test():
    return render_template('user_page/user_page.html')
