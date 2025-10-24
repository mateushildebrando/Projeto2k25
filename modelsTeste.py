from config import *
class Usuario(db.Model):
    __tablename__ = 'usuario'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    foto = db.Column(db.String(200), nullable=False, default='/static/imagens/fotosperfil/default.jpg')
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Usuario {self.username}>'

class Token(db.Model):
    __tablename__ = 'token'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.TEXT, nullable=False)
    token_ativo = db.Column(db.TEXT, nullable=False)

with app.app_context():
    db.create_all()