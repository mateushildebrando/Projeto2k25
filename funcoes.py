from modelsTeste import *
from config import *

CAMINHO_FOTOS = os.path.join(os.getcwd(), "static", "imagens", "fotosperfil")

def criar_usuario(form):
    nome = form.get("first_name")
    sobrenome = form.get("last_name")
    username = form.get("username")
    email = form.get("email")
    senha_raw = form.get("password")
    senha = generate_password_hash(senha_raw)
    foto = "/static/imagens/fotosperfil/default.jpg"

    novo_usuario = UsuarioTeste(nome=nome,sobrenome=sobrenome, username=username, email=email, senha=senha, foto=foto)

    try:
        db.session.add(novo_usuario)
        db.session.commit()
        
    except Exception as e:
        db.session.rollback()
        
def autenticar_usuario(form):
    login_usuario = form.get("login_user")
    senha_raw = form.get("password")

    usuario = UsuarioTeste.query.filter(
        (UsuarioTeste.email == login_usuario) | 
        (UsuarioTeste.username == login_usuario)
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

    usuario = UsuarioTeste.query.filter_by(email=session.get("email")).first()

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

    emailsuporte = 'suporte.manstrail@gmail.com'
    senhasuporte = 'gnsibgmfysdiqprr'

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