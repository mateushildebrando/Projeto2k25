from config import *

class User(db.Entity):
    iduser = PrimaryKey(int, auto=True)
    usuario = Required(str)
    email = Required(str)
    senha = Required(str)
    favoritos = Set('Favorito')

class Conteudo(db.Entity):
    idconteudo = PrimaryKey(int, auto=True)
    titulo = Required(str)
    corpo = Optional(str)
    categoria = Optional(str)
    favoritos = Set('Favorito')

class Favorito(db.Entity):
    idfavorito = PrimaryKey(int, auto=True)
    iduser = Required(User)
    idconteudo = Required(Conteudo)

db.bind(
    provider='mysql',
    user='root',
    password='rootroot',
    host='localhost',
    database='bdprojeto2k25'
)

db.generate_mapping()
