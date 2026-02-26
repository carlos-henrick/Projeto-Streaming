from models.tabelas import Favorito, Filme, Serie
from database.db_connection import db


class FavoritoService:

    @staticmethod
    def adicionar(usuario_id, dados):
        tipo = dados.get("tipo_midia")
        midia_id = dados.get("midia_id")

        if tipo not in ("filme", "serie"):
            raise ValueError("Tipo de mídia inválido.")

        try:
            midia_id = int(midia_id)
        except (ValueError, TypeError):
            raise ValueError("ID inválido.")

        # validar mídia existe
        Model = Filme if tipo == "filme" else Serie
        midia = Model.query.get(midia_id)

        if not midia:
            raise ValueError("Mídia não encontrada.")

        # impedir duplicado
        existente = Favorito.query.filter_by(
            usuario_id=usuario_id,
            tipo_midia=tipo,
            midia_id=midia_id
        ).first()

        if existente:
            raise ValueError("Já está nos favoritos.")

        favorito = Favorito(
            usuario_id=usuario_id,
            tipo_midia=tipo,
            midia_id=midia_id
        )

        db.session.add(favorito)
        db.session.commit()

        return favorito


    @staticmethod
    def remover(usuario_id, favorito_id):
        favorito = Favorito.query.filter_by(
            id=favorito_id,
            usuario_id=usuario_id
        ).first()

        if not favorito:
            raise ValueError("Favorito não encontrado.")

        db.session.delete(favorito)
        db.session.commit()


    @staticmethod
    def listar(usuario_id):
        favoritos = Favorito.query.filter_by(usuario_id=usuario_id).all()

        resultado = []

        for fav in favoritos:
            if fav.tipo_midia == "filme":
                midia = Filme.query.get(fav.midia_id)
            else:
                midia = Serie.query.get(fav.midia_id)

            if not midia:
                continue

            resultado.append({
                "id": fav.id,
                "tipo_midia": fav.tipo_midia,
                "midia_id": fav.midia_id,
                "titulo": midia.titulo,
                "capa": midia.capa
            })

        return resultado