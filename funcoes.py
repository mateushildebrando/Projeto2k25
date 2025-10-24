from modelsTeste import *
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

    if not nome or not sobrenome or not username or not email or not senha:
        flash("Ocorreu um erro. Tente novamente!")
        return redirect(url_for("cadastro"))

    novo_usuario = Usuario(nome=nome,sobrenome=sobrenome, username=username, email=email, senha=senha, foto=foto)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        
def autenticar_usuario(form):
    login_usuario = form.get("login_user")
    senha_raw = form.get("password")

    usuario = Usuario.query.filter(
        (Usuario.email == login_usuario) | 
        (Usuario.username == login_usuario)
    ).first()

    if usuario and check_password_hash(usuario.senha, senha_raw):
        return {
            "nome": usuario.nome,
            "sobrenome": usuario.sobrenome,
            "username": usuario.username,
            "email": usuario.email,
            "foto_perfil": usuario.foto
        }
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
    
    novo_token = Token(email=email, token_ativo=token)

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
        token_obj =  Token.query.filter(
            (Token.token_ativo == token)).first()
        email_session = token_obj.email
    
    usuario = Usuario.query.filter(
        (Usuario.email == email_session)).first()
    
    if not usuario:
        return 'Usuário não encontrado.'
        
    token_verificado = Token.query.filter(
        (Token.token_ativo == token)).first()
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