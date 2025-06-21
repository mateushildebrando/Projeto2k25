from modelsTeste import *
from config import *

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
    nome = request.form.get("first-name")
    email = request.form.get("email")
    senha = request.form.get("password")
    
    with db_session:
        novo_user = UsuarioTeste(nome=nome, email=email, senha=senha)
        commit()

        return redirect(url_for("home"))


@app.route("/acesso/login")
def login():
    return render_template("login.html")

@app.route("/acesso/login/usuario", methods=["POST"])
def loginUser():
    email = request.form.get("email")
    senha = request.form.get("password")

    with db_session:
        usuario = select(u for u in UsuarioTeste if u.email == email and u.senha == senha).first()
        
        if usuario:
            session["username"] = usuario.nome
            session["email"] = usuario.email

            return render_template_string("""
                <script>
                    alert("Login bem sucedido!");
                    window.location.href = "/";
                </script>
            """)
        else:
            return render_template_string("""
                <script>
                    alert("Email ou senha incorretos.");
                    window.location.href = "/acesso/login";
                </script>
            """)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")