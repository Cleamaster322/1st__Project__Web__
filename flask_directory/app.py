from flask import Flask, render_template, url_for, request,redirect

app = Flask(__name__)


@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')


@app.route("/forgotten_password")
def for_password():
    return render_template('forgotten_password/forgotten_password.html')


@app.route("/register")
def register():
    if request.form:
        print(1)


@app.route("/check_in")
def for_database_test():
    return render_template('check_in_page/check_in_page.html')
