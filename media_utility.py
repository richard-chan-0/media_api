from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/videos")
def rename_videos():
    return "<p>Renaming videos...</p>"


@app.route("/books")
def rename_books():
    return "<p>Renaming books...</p>"
