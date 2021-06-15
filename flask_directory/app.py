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


@app.route("/messange")
def for_messanges():
    return render_template('messange_page/messange_page.html')


@app.route("/followers")
def for_followers():
    return render_template('my_followers/my_followers.html')


@app.route("/me_following")
def for_following():
    return render_template('me_following/me_following.html')


@app.route("/news")
def for_news():
    return render_template('news/news.html')