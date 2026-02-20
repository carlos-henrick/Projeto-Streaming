from models.tabelas import Serie
from database.db_connection import db
from validators.validators import IDADES_VALIDAS


class SerieService:

    @staticmethod
    def listar(titulo=None, genero=None, idade_max=None):
        query = Serie.query

        if titulo:
            query = query.filter(Serie.titulo.ilike(f"%{titulo}%"))

        if genero:
            query = query.filter(Serie.genero.ilike(f"%{genero}%"))

        if idade_max is not None:
            if idade_max not in IDADES_VALIDAS.values():
                raise ValueError("idade_max inválido.")
            query = query.filter(Serie.idade <= idade_max)

        return query.order_by(Serie.titulo).all()

    @staticmethod
    def criar(dados):
        if Serie.query.filter_by(titulo=dados["titulo"]).first():
            raise ValueError("Série já cadastrada.")

        serie = Serie(**dados)
        db.session.add(serie)
        db.session.commit()
        return serie

    @staticmethod
    def obter_por_id(serie_id):
        return Serie.query.get(serie_id)

    @staticmethod
    def atualizar(serie, dados):
        for campo, valor in dados.items():
            setattr(serie, campo, valor)

        db.session.commit()
        return serie

    @staticmethod
    def deletar(serie):
        db.session.delete(serie)
        db.session.commit()
