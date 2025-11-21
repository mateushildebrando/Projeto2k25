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
    ativo = db.Column(db.Boolean, nullable=False)

    favoritos = db.relationship('Favorito', back_populates='usuario', cascade='all, delete-orphan')

class TokenEmail(db.Model):
    __tablename__ = 'token_email'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.TEXT, nullable=False)
    token_ativo = db.Column(db.TEXT, nullable=False)

class TokenSenha(db.Model):
    __tablename__ = 'token_senha'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.TEXT, nullable=False)
    token_ativo = db.Column(db.TEXT, nullable=False)

class Topico(db.Model):
    __tablename__ = 'topico'

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.String(200), nullable=False)
    link = db.Column(db.String(150), nullable=False)
    categoria = db.Column(db.String(15), nullable=False)

    favoritos = db.relationship('Favorito', back_populates='topico', cascade='all, delete-orphan')

class Favorito(db.Model):
    __tablename__ = 'favorito'

    id = db.Column(db.Integer, primary_key=True)
    topico_id = db.Column(db.Integer, db.ForeignKey('topico.id'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)

    usuario = db.relationship('Usuario', back_populates='favoritos')
    topico = db.relationship('Topico', back_populates='favoritos')

with app.app_context():
    db.create_all()

    itens = [
        Topico(texto="Planeje antes de acelerar.", 
               link="https://universodoseguro.com.br/automobilismo-e-tecnologia-uma-paixao-que-inspira-transformacao",
               categoria="automobilismo"),


        Topico(texto="Ajuste seu “carro” — corpo e mente", 
               link="https://www.periodicos.rc.biblioteca.unesp.br/index.php/brajosp/article/view/19827",
               categoria="automobilismo"),


        Topico(texto="Jamais perca o traçado do seu propósito.", 
               link="https://pt.wikipedia.org/wiki/Tra%C3%A7ado_%28automobilismo%29",
               categoria="automobilismo"),


        Topico(texto="Limpeza: duas vezes ao dia, com sabonete facial específico.", 
               link="https://www.realsimple.com/beauty-fashion/skincare/simple-skincare-routine",
               categoria="cuidados"),

        Topico(texto="Hidratação: use hidratante oil free.", 
               link="https://www.verywellhealth.com/acne-and-oily-skin-15964",
               categoria="cuidados"),

        Topico(texto="Protetor solar: essencial contra envelhecimento e manchas.", 
               link="https://www.realsimple.com/beauty-fashion/skincare/simple-skincare-routine",
               categoria="cuidados"),

        Topico(texto="Esfoliação: 1x por semana para remover células mortas.", 
               link="https://www.vogue.com/article/best-face-exfoliator",
               categoria="cuidados"),

        Topico(texto="Futebol: melhora o condicionamento e a tomada de decisão.", 
               link="https://www.lance.com.br/outros-lances/2025/07/13/futebol-e-o-melhor-aliado-contra-a-fadiga-mental",
               categoria="esportes"),

        Topico(texto="Basquete: desenvolve força, agilidade e raciocínio.", 
               link="https://www.ativo.com/ativo/beneficios-do-basquete-esporte-ajuda-o-fisico-e-mente",
               categoria="esportes"),

        Topico(texto="Calistenia: fortalece articulações e postura.", 
               link="https://www.verywellhealth.com/calisthenics-benefits-8718013",
               categoria="esportes"),

        Topico(texto="Corrida: acessível e eficaz para liberar endorfinas.", 
               link="https://physicum.nl/en/articles/10-benefits-of-running-physical-and-mental-effects",
               categoria="esportes"),

        Topico(texto="Musculação: essencial para força e prevenção de lesões.", 
               link="https://www.unimedlondrina.com.br/noticias/tudo-saude/22/07/2024/beneficios-do-esporte-para-a-saude-escolha-o-melhor-para-voce",
               categoria="esportes"),

        Topico(texto="Leitura bíblica: a fé vem pelo ouvir a Palavra (Romanos 10:17).", 
               link="https://youtu.be/-4zbE76FAfo?si=SXJEGF8MLADMUDNY",
               categoria="fe"),

        Topico(texto="Oração constante: fale com Deus com sinceridade, não formalidade.", 
               link="https://youtu.be/bcVo7pKoH6A?si=Z-nt1gZcKaJyvngD",
               categoria="fe"),

        Topico(texto="Comunhão: Provérbios 27:17 — “Assim como o ferro afia o ferro, o homem afia o seu companheiro.”", 
               link="https://youtu.be/sjuRexo61bQ?si=7n0uQqPVj19a9wPH",
               categoria="fe"),

        Topico(texto="Obediência: fé verdadeira gera ação e transformação.", 
               link="https://youtu.be/3a51YTfZ-_s?si=XfMvJlfALBOAxnyT",
               categoria="fe"),

        Topico(texto="Streetwear: mistura conforto e atitude. Peças-chave: calça cargo, camiseta oversized, boné aba curva, jaqueta corta-vento, tênis impactante. Acessórios: correntes prateadas, shoulder bag, anéis.", 
               link="https://www.theballentinecollective.com/blogs/blog/can-streetwear-be-combined-with-old-money",
               categoria="moda"),

        Topico(texto="Sport Life: visual leve, atlético e versátil. Peças-chave: camiseta dry fit, calça jogger, moletom neutro, tênis esportivo limpo. Valoriza o corpo e transmite disciplina.", 
               link="https://en.wikipedia.org/wiki/Athleisure",
               categoria="moda"),

        Topico(texto="Old Money: elegância discreta. Peças-chave: camisa social branca, calça de alfaiataria, mocassim, polo ou suéter, cores neutras e bom caimento.", 
               link="https://www.byrdie.com/old-money-style-trend-8748874",
               categoria="moda"),
    ]

    if Topico.query.count() == 0:
        db.session.add_all(itens)
        db.session.commit()
        print("Tópicos inseridos.")
    else:
        print("Tópicos já existem, não foram inseridos novamente.")