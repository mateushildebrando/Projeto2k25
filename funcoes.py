from models import *
from config import *

CAMINHO_FOTOS = os.path.join(os.getcwd(), "static", "imagens", "fotosperfil")

emailsuporte = 'suporte.manstrail@gmail.com'
senhasuporte = 'gnsibgmfysdiqprr'

def criar_usuario(form):
    nome = form.get("first_name")
    sobrenome = form.get("last_name")
    username = form.get("username")
    email = form.get("email")
    senha_raw = form.get("password")
    senha = generate_password_hash(senha_raw)
    foto = "/static/imagens/fotosperfil/default.jpg"
    ativo = False

    if not all([nome, sobrenome, username, email, senha_raw]):
        flash("Ocorreu um erro. Tente novamente!")
        return redirect(url_for("cadastro"))

    token = str(uuid.uuid4())
       
    novo_usuario = Usuario(nome=nome,sobrenome=sobrenome, username=username, email=email, senha=senha, foto=foto, ativo=ativo)
    novo_token = TokenEmail(email=email, token_ativo=token)

    try:
        db.session.add(novo_usuario)
        db.session.add(novo_token)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()

    link = url_for ('confirmarEmail', token=token, _external=True)

    msg = MIMEMultipart()
    msg['From'] = emailsuporte
    msg['To'] = email
    msg['Subject'] = f"Confirmação de Email"
    
    mensagemHTML = f"""
        <h2>Confirmação de email</h2>
        <p>Clique no link abaixo para Confirmar seu email:</p>
        <a href="{link}">{link}</a>
    """
    msg.attach(MIMEText(mensagemHTML, "html"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(emailsuporte, senhasuporte)
            servidor.send_message(msg)
            return {"status": "sucesso", "mensagem": "Email enviado com sucesso!"}
    except Exception as e:
        print("Erro ao enviar email:", e)
        return {"status": "erro", "mensagem": str(e)}
        
    
def ativar_conta(token):
    token_obj = TokenEmail.query.filter(
        (TokenEmail.token_ativo == token)
    ).first()

    if not token_obj:
        flash('Token inválido ou expirado!')
        return redirect(url_for('cadastro'))
    
    usuario_obj = Usuario.query.filter_by(email=token_obj.email).first()


    if not usuario_obj:
        flash('Usuário não encontrado!')
        return redirect(url_for('cadastro'))
    
    else:
        usuario_obj.ativo = True
        db.session.delete(token_obj)
        db.session.commit()
        flash('Cadastro realizado com sucesso!')
        return redirect(url_for('login'))



def autenticar_usuario(form):
    login_usuario = form.get("login_user")
    senha_raw = form.get("password")

    usuario = Usuario.query.filter(
        (Usuario.email == login_usuario) | 
        (Usuario.username == login_usuario)
    ).first()

    if not usuario:
        flash('Usuário não encontrado!')
        return None
    
    if usuario.ativo == False:
        flash('Usuario não foi ativo, verifique seu email!')
        return None

    if usuario and check_password_hash(usuario.senha, senha_raw):
        return {
            "id": usuario.id,
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "username": usuario.username,
            "email": usuario.email,
            "foto_perfil": usuario.foto
        }
    else:
        flash("Email ou senha incorretos.", "error")
        return None

def atualizar_perfil(form, files, session):
    novo_nome = form.get("nome")
    novo_sobrenome = form.get("sobrenome")
    novo_username = form.get("username")
    novo_email = form.get("email")
    nova_foto = files.get("foto_perfil")

    usuario = Usuario.query.filter_by(email=session.get("email")).first()

    if not usuario:
        return False, "Usuário não encontrado."

    usuario.nome = novo_nome
    usuario.sobrenome = novo_sobrenome
    usuario.username = novo_username
    usuario.email = novo_email

    if nova_foto and nova_foto.filename != '':
        nome_arquivo = secure_filename(nova_foto.filename)
        caminho_foto = os.path.join(CAMINHO_FOTOS, nome_arquivo)
        nova_foto.save(caminho_foto)
        url_foto = f'/static/imagens/fotosperfil/{nome_arquivo}'
        usuario.foto = url_foto
        session["foto_perfil"] = url_foto

    session.update({
        "nome": novo_nome,
        "sobrenome": novo_sobrenome,
        "username": novo_username,
        "email": novo_email
    })

    db.session.commit()

    return True, "Perfil atualizado com sucesso!"
    
def exclusao_permanente():
    email = session['email']    
    usuario = Usuario.query.filter_by(email=email).first()
    session.clear()
    db.session.delete(usuario)
    db.session.commit()

def mensagem_suporte(form):

    userremetente = session.get('username')
    emailremetente = session.get('email')
    mensagem = form.get('mensagem')

    msg = MIMEMultipart()
    msg['From'] = emailsuporte
    msg['To'] = emailsuporte
    msg['Subject'] = f"Mensagem de suporte - {userremetente} ({emailremetente})"
    msg.attach(MIMEText(mensagem, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.starttls()
            servidor.login(emailsuporte, senhasuporte)
            servidor.send_message(msg)
        return {"status": "sucesso", "mensagem": "Email enviado com sucesso!"}
    except Exception as e:
        print("Erro ao enviar email:", e)
        return {"status": "erro", "mensagem": str(e)}
    
def email_solicitado(form):
    email = form.get('email')
    token = str(uuid.uuid4())
    
    novo_token = TokenSenha(email=email, token_ativo=token)

    try:
        db.session.add(novo_token)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        print("Erro ao salvar token no banco:", e)
        return {"status": "erro", "mensagem": "Erro ao gerar token."}

    link = url_for('formNovaSenha', token=token, _external=True)

    msg = MIMEMultipart()
    msg['From'] = emailsuporte
    msg['To'] = email
    msg['Subject'] = f"Redefinição de Senha"
    
    mensagemHTML = f"""
        <h2>Redefinição de Senha</h2>
        <p>Clique no link abaixo para redefinir sua senha:</p>
        <a href="{link}">{link}</a>
    """
    msg.attach(MIMEText(mensagemHTML, "html"))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
            servidor.ehlo()
            servidor.starttls()
            servidor.ehlo()
            servidor.login(emailsuporte, senhasuporte)
            servidor.send_message(msg)
            return {"status": "sucesso", "mensagem": "Email enviado com sucesso!"}
    except Exception as e:
        print("Erro ao enviar email:", e)
        return {"status": "erro", "mensagem": str(e)}

def encontrarUsuarioEToken(token):
    email_session = session.get('email')
    
    if not email_session:
        token_obj =  TokenSenha.query.filter(
            (TokenSenha.token_ativo == token)).first()
        email_session = token_obj.email
    
    usuario = Usuario.query.filter(
        (Usuario.email == email_session)).first()
    
    if not usuario:
        return 'Usuário não encontrado.'
        
    token_verificado = TokenSenha.query.filter(
        (TokenSenha.token_ativo == token)).first()
    if not token_verificado:
        return 'Token inválido ou expirado.'
    
    return usuario, token_verificado

def update_senha(form, usuario, token_verificado):
    nova_senha_raw = form.get('senha')
    confirmacao_senha_raw = form.get('confirmacao_senha')
    nova_senha = generate_password_hash(nova_senha_raw)

    if nova_senha_raw != confirmacao_senha_raw:
        flash('As senhas não coincidem. Digite a mesma senha na confirmação.', 'erro')
        return redirect(url_for('formNovaSenha', token=token_verificado.token_ativo))

    elif len(nova_senha_raw) < 8:
        flash('A senha precisa ter mais de 8 caracteres.', 'erro')
        return redirect(url_for('formNovaSenha', token=token_verificado.token_ativo))

    else:
        usuario.senha = nova_senha
        
        db.session.delete(token_verificado)
        db.session.commit()
        session.clear()
        flash('Senha redefinida com sucesso!')
        return redirect(url_for('login'))
    
def favoritamento(id_topico):
    id_usuario = session.get('id')

    if id_usuario is None:
        flash("Você precisa de login para poder favoritar")
        return jsonify({"erro": "login necessário"}), 401

    topico = Topico.query.get(id_topico)
    if not topico:
        return jsonify({"erro": "topico nao encontrado"}), 404

    favorito_existente = Favorito.query.filter_by(
        topico_id=id_topico,
        usuario_id=id_usuario,
    ).first()

    if favorito_existente:
        db.session.delete(favorito_existente)
        db.session.commit()
        return jsonify({"favorito": False})

    novo = Favorito(topico_id=id_topico, usuario_id=id_usuario)
    db.session.add(novo)
    db.session.commit()
    return jsonify({"favorito": True})

def enviar_mensagem():
    usuario_id = session.get("id")
    conteudo = request.form.get("conteudo")

    if not usuario_id:
        return jsonify({"erro": "login necessário"}), 401

    msg = Mensagem(conteudo=conteudo, usuario_id=usuario_id)
    db.session.add(msg)
    db.session.commit()

    return jsonify({"status": "ok"})


def listar_mensagens():
    msgs = Mensagem.query.order_by(Mensagem.criado_em.asc()).all()

    return jsonify([
        {
            "usuario": m.usuario.nome,
            "conteudo": m.conteudo,
            "criado_em": m.criado_em.strftime("%d/%m %H:%M"),
        }
        for m in msgs
    ])