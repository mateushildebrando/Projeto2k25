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

@app.route("/acesso/cadastro")
def cadastro():
    return render_template("cadastro.html")

@app.route("/acesso/login")
def login():
    return render_template("login.html")

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")