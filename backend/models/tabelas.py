from datetime import datetime
from database.db_connection import db


# USUÁRIO

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)


    favoritos = db.relationship("Favorito", backref="usuario", lazy=True)
    historico = db.relationship("Historico", backref="usuario", lazy=True)




# FILMES

class Filme(db.Model):
    __tablename__ = "filmes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_lancamento = db.Column(db.Date, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(80), nullable=False)
    capa = db.Column(db.String(200), nullable=False)
    nome_arquivo_video = db.Column(db.String(200), nullable=False)

    favoritos = db.relationship("Favorito", backref="filme", cascade="all, delete-orphan", lazy=True)



# SÉRIES

class Serie(db.Model):
    __tablename__ = "series"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    idade = db.Column(db.Integer, nullable=False)
    genero = db.Column(db.String(80), nullable=False)
    capa = db.Column(db.String(200), nullable=False)

    episodios = db.relationship("Episodio", backref="serie", cascade="all, delete-orphan", lazy=True)
    favoritos = db.relationship("Favorito", backref="serie", cascade="all, delete-orphan", lazy=True)




# EPISÓDIOS

class Episodio(db.Model):
    __tablename__ = "episodios"

    id = db.Column(db.Integer, primary_key=True)
    serie_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=False)

    temporada = db.Column(db.Integer, nullable=False)
    numero_episodio = db.Column(db.Integer, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_lancamento = db.Column(db.Date, nullable=False)
    capa = db.Column(db.String(200), nullable=False)
    duracao = db.Column(db.Integer, nullable=False)
    nome_arquivo_video = db.Column(db.String(200), nullable=False)




# FAVORITOS 

class Favorito(db.Model):
    __tablename__ = "favoritos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    
    filme_id = db.Column(db.Integer, db.ForeignKey("filmes.id"), nullable=True)
    serie_id = db.Column(db.Integer, db.ForeignKey("series.id"), nullable=True)

    criado_em = db.Column(db.DateTime, default=datetime.utcnow)



# HISTÓRICO 

class Historico(db.Model):
    __tablename__ = "historicos"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    tipo_midia = db.Column(db.String(20), nullable=False)
    midia_id = db.Column(db.Integer, nullable=False)
    tempo_atual = db.Column(db.Integer, nullable=False)
    finalizado = db.Column(db.Boolean, default=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint("usuario_id", "tipo_midia", "midia_id"),
    )




# PLANOS

class Plano(db.Model):
    __tablename__ = "planos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    resolucao_maxima = db.Column(db.String(10))
    preco = db.Column(db.Float)

    assinaturas = db.relationship("Assinatura", backref="plano", lazy=True)



# ASSINATURAS

class Assinatura(db.Model):
    __tablename__ = "assinaturas"

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    plano_id = db.Column(db.Integer, db.ForeignKey("planos.id"), nullable=False)

    inicio = db.Column(db.DateTime, default=datetime.utcnow)
    validade = db.Column(db.DateTime)
    ativa = db.Column(db.Boolean, default=True)

