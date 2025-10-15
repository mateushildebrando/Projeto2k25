from config import *
class UsuarioTeste(db.Model):
    __tablename__ = 'usuarios_teste'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    sobrenome = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    foto = db.Column(db.String(200), nullable=False, default='/static/imagens/fotosperfil/default.jpg')
    senha = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<UsuarioTeste {self.username}>'

with app.app_context():
    db.create_all()