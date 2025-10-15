from modelsTeste import *
from config import *
from funcoes import *

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

@app.route("/acesso/cadastro/novo_usuario", methods=["POST"])
def novo_usuario():
    criar_usuario(request.form)
    return redirect(url_for("login"))

@app.route("/acesso/login")
def login():
    return render_template("login.html")

@app.route("/acesso/login/usuario", methods=["POST"])
def loginUser():
    usuario = autenticar_usuario(request.form)
    if usuario:
        session.update(usuario)
        return redirect(url_for("perfil"))
    flash("Email ou senha incorretos.", "error")
    return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

@app.route("/perfil")
def perfil():
    return render_template("perfil.html")

@app.route("/perfil/atualizado", methods=["POST"])
def update_perfil():
    sucesso, msg = atualizar_perfil(request.form, request.files, session)
    flash(msg, "success" if sucesso else "error")
    return redirect(url_for("perfil" if sucesso else "login"))

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/suporte")
def suporte():
    return render_template('suporte.html')

@app.route("/suporte/contatosuporte", methods=["POST"])
def suporteContato():
    mensagem_suporte(request.form)

@app.route("/forum")
def forum():
    return render_template('forum.html')