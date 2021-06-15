from flask import Flask, render_template, url_for, request,redirect

app = Flask(__name__)


@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')


@app.route("/forgotten_password")
def for_password():
    return render_template('forgotten_password/forgotten_password.html')




@app.route("/check_in")
def for_database_test():
    return render_template('check_in_page/check_in_page.html')


@app.route('/add')
def posts_add():
    return render_template('/register_form/register_form.html')

@app.route('/register', methods=['post'])
def addpost():
    if request.form:
        login = request.form.get('login')
        password = request.form.get('password')
        mail = request.form.get('mail')
        
        post = {'login':login, 'password':password, 'mail':mail}
        print(post)
        

    return redirect('/')
