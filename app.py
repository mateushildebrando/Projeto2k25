from modelsTeste import *
from config import *
from funcoes import *

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/fe")
def fe():
    usuario_id = session.get("id")
    topicos = Topico.query.filter_by(categoria="fe").all()

    favoritos_ids = [
        fav.topico_id
        for fav in Favorito.query.filter_by(usuario_id=usuario_id).all()
    ]

    return render_template("fe.html",
                           topicos=topicos,
                           favoritos_ids=favoritos_ids)

@app.route("/cuidados")
def cuidados():
    usuario_id = session.get("id")
    topicos = Topico.query.filter_by(categoria="cuidados").all()

    favoritos_ids = [
        fav.topico_id
        for fav in Favorito.query.filter_by(usuario_id=usuario_id).all()
    ]

    return render_template("cuidados.html",
                           topicos=topicos,
                           favoritos_ids=favoritos_ids)

@app.route("/esportes")
def esportes():
    usuario_id = session.get("id")
    topicos = Topico.query.filter_by(categoria="esportes").all()

    favoritos_ids = [
        fav.topico_id
        for fav in Favorito.query.filter_by(usuario_id=usuario_id).all()
    ]

    return render_template("esportes.html",
                           topicos=topicos,
                           favoritos_ids=favoritos_ids)

@app.route("/moda")
def moda():
    usuario_id = session.get("id")
    topicos = Topico.query.filter_by(categoria="moda").all()

    favoritos_ids = [
        fav.topico_id
        for fav in Favorito.query.filter_by(usuario_id=usuario_id).all()
    ]

    return render_template("moda_masculina.html",
                           topicos=topicos,
                           favoritos_ids=favoritos_ids)

@app.route("/automobilismo")
def automobilismo():
    usuario_id = session.get("id")
    topicos = Topico.query.filter_by(categoria="automobilismo").all()

    favoritos_ids = [
        fav.topico_id
        for fav in Favorito.query.filter_by(usuario_id=usuario_id).all()
    ]

    return render_template("automobilismo.html",
                           topicos=topicos,
                           favoritos_ids=favoritos_ids)


@app.route("/favoritos")
def favoritos():
    usuario_id = session.get('id')

    if usuario_id is None:
        flash("Faça login para ver seus favoritos.")
        return redirect(url_for("login"))
    favoritos = Favorito.query.filter_by(usuario_id=usuario_id).all()
    return render_template("favoritos.html", favoritos=favoritos)



@app.route("/favoritar/<int:id_topico>", methods=["POST"])
def favoritar(id_topico):
    return favoritamento(id_topico)



@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/cadastro")
def cadastro():
    return render_template("cadastro.html")
  
@app.route("/cadastro/novo_usuario", methods=["POST"])
def novo_usuario():
    resultado = criar_usuario(request.form)
    if resultado.get("status") == "sucesso":
        flash("Verifique seu email para confirmar a conta!")
    else:
        flash("Erro ao enviar o email de confirmação.")
    return redirect(url_for("home"))

@app.route("/confirmarEmail/<token>")
def confirmarEmail(token):
    return ativar_conta(token)
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login/usuario", methods=["POST"])
def loginUser():
    usuario = autenticar_usuario(request.form)
    if usuario:
        session.update(usuario)
        return redirect(url_for("perfil"))
    else:
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

@app.route('/excluir_conta')
def excluir_conta():
    exclusao_permanente()
    flash('Usuário deletado!')
    return redirect(url_for('home'))

@app.route('/esqueci_senha')
def esqueci_senha():
    return render_template('esqueci_senha.html')


@app.route('/esqueci_senha/nova_senha', methods=['POST'])
def email_redefinicao():
    email_solicitado(request.form)

    flash('Verifique seu email!')
    return redirect(url_for('login'))

@app.route('/redefinir_senha/<token>')
def formNovaSenha(token):
    return render_template('novaSenha.html', token=token)

@app.route('/redefinir_senha/nova_senha/<token>', methods=['POST'])
def redefinir_senha(token):
    resultado = encontrarUsuarioEToken(token)
    if resultado is None:
        flash('Usuário ou token não encontrado!')
        return redirect(url_for('cadastro'))
    if isinstance(resultado, tuple):
        usuario, token_verificado = resultado
    else:
        return resultado
    
    verificacao = update_senha(request.form, usuario, token_verificado)
    if verificacao:
        return verificacao

@app.route("/suporte")
def suporte():
    if session:
        return render_template('suporte.html')
    else:
        flash("Você precisa estar logado para acionar o suporte!")
        return redirect(url_for("login"))
        
@app.route("/suporte/contatosuporte", methods=["POST"])
def suporteContato():
    mensagem_suporte(request.form)

    flash('Email enviado com sucesso!')
    return redirect(url_for('suporte'))
       
if __name__ == '__main__':
    app.run(debug=True)