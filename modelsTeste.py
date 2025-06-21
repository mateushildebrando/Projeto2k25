from config import *

db = Database()

class UsuarioTeste(db.Entity):
    id = PrimaryKey(int, auto=True) 
    nome = Required(str)
    email = Required(str, unique=True)
    senha = Required(str)

db.bind(provider='sqlite', filename='teste.sqlite', create_db=True)
db.generate_mapping(create_tables=True)