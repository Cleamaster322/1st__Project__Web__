from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def title():
    return render_template('/title_frame/title_frame.html')
