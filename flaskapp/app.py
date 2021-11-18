from flask import Flask

app = Flask(__name__)


@app.route("/")
def root():
    return "Hello there <b>mate!</b>"


@app.route("/hello/")
@app.route("/hello/<name>")
def hello(name=None):
    if name:
        return "Welcome, " + name
    else:
        return "Welcome visitor!"
