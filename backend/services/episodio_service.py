from models.tabelas import Episodio, Serie
from database.db_connection import db


class EpisodioService:

    @staticmethod
    def listar_por_serie(serie_id):
        serie = Serie.query.get(serie_id)
        if not serie:
            raise ValueError("Série não encontrada.")

        return (
            Episodio.query
            .filter_by(serie_id=serie_id)
            .order_by(Episodio.temporada, Episodio.numero_episodio)
            .all()
        )

    @staticmethod
    def criar(dados):
        serie = Serie.query.get(dados["serie_id"])
        if not serie:
            raise ValueError("Série não encontrada.")

        existe = Episodio.query.filter_by(
            serie_id=dados["serie_id"],
            temporada=dados["temporada"],
            numero_episodio=dados["numero_episodio"]
        ).first()

        if existe:
            raise ValueError("Esse episódio já existe.")

        episodio = Episodio(**dados)
        db.session.add(episodio)
        db.session.commit()
        return episodio

    @staticmethod
    def obter_por_id(episodio_id):
        return Episodio.query.get(episodio_id)

    @staticmethod
    def atualizar(episodio, dados):
        for campo, valor in dados.items():
            setattr(episodio, campo, valor)

        db.session.commit()
        return episodio

    @staticmethod
    def deletar(episodio):
        db.session.delete(episodio)
        db.session.commit()
