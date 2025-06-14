from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/auxiliar")
def auxiliar():
    return render_template("auxiliar.html")

@app.route("/acesso")
def acesso():
    return render_template("acesso.html")