from models.tabelas import Filme
from database.db_connection import db
from validators.validators import IDADES_VALIDAS


class FilmeService:

    @staticmethod
    def listar(titulo=None, genero=None, idade_max=None):
        query = Filme.query

        if titulo:
            query = query.filter(Filme.titulo.ilike(f"%{titulo}%"))

        if genero:
            query = query.filter(Filme.genero.ilike(f"%{genero}%"))

        if idade_max is not None:
            if idade_max not in IDADES_VALIDAS.values():
                raise ValueError("idade_max inválido.")
            query = query.filter(Filme.idade <= idade_max)

        return query.order_by(Filme.titulo).all()

    @staticmethod
    def criar(dados):
        if Filme.query.filter_by(titulo=dados["titulo"]).first():
            raise ValueError("Filme já cadastrado.")

        filme = Filme(**dados)
        db.session.add(filme)
        db.session.commit()
        return filme

    @staticmethod
    def obter_por_id(filme_id):
        return Filme.query.get(filme_id)

    @staticmethod
    def atualizar(filme, dados):
        for campo, valor in dados.items():
            setattr(filme, campo, valor)

        db.session.commit()
        return filme

    @staticmethod
    def deletar(filme):
        db.session.delete(filme)
        db.session.commit()
