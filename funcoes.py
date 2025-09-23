from modelsTeste import *
from werkzeug.utils import secure_filename
import os

CAMINHO_FOTOS = os.path.join(os.getcwd(), "static", "imagens", "fotosperfil")

def criar_usuario(form):
    nome = form.get("first_name")
    sobrenome = form.get("last_name")
    username = form.get("username")
    email = form.get("email")
    senha = form.get("password")
    foto = "/static/imagens/fotosperfil/default.jpg"

    with db_session:
        UsuarioTeste(nome=nome, sobrenome=sobrenome, username=username,
                     email=email, senha=senha, foto=foto)
        commit()

def autenticar_usuario(form):
    login_usuario = form.get("login_user")
    senha = form.get("password")

    with db_session:
        usuario = select(u for u in UsuarioTeste
                         if (u.email == login_usuario or u.username == login_usuario)
                         and u.senha == senha).first()

        if usuario:
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

    with db_session:
        usuario = UsuarioTeste.get(email=session.get("email"))

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

        # Atualiza session
        session.update({
            "nome": novo_nome,
            "sobrenome": novo_sobrenome,
            "username": novo_username,
            "email": novo_email
        })

        return True, "Perfil atualizado com sucesso!"