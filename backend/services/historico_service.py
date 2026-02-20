from models.tabelas import Historico, Filme, Episodio
from database.db_connection import db


class HistoricoService:

    # BUSCAR PROGRESSO

    @staticmethod
    def buscar_progresso(usuario_id, tipo, midia_id):
        h = Historico.query.filter_by(
            usuario_id=usuario_id,
            tipo_midia=tipo,
            midia_id=midia_id
        ).first()

        if not h:
            return {"tempo_atual": 0, "finalizado": False}

        return {
            "tempo_atual": h.tempo_atual,
            "finalizado": h.finalizado
        }

    # ATUALIZAR PROGRESSO

    @staticmethod
    def atualizar_progresso(usuario_id, dados):
        tipo = dados.get("tipo_midia")
        midia_id = dados.get("midia_id")
        tempo = dados.get("tempo_atual")

        # VALIDAR TIPO
        if tipo not in ("filme", "episodio"):
            raise ValueError("Tipo de mídia inválido.")

        # VALIDAR ID
        try:
            midia_id = int(midia_id)
        except:
            raise ValueError("ID da mídia inválido.")

        # VALIDAR TEMPO
        try:
            tempo = int(tempo)
        except:
            raise ValueError("Tempo inválido.")

        if tempo < 0:
            raise ValueError("Tempo não pode ser negativo.")

        # BUSCAR MÍDIA
        if tipo == "filme":
            midia = Filme.query.get(midia_id)
        else:
            midia = Episodio.query.get(midia_id)

        if not midia:
            raise ValueError("Mídia não encontrada.")


        duracao_total = midia.duracao * 60 

        # LIMITAR TEMPO
        if tempo > duracao_total:
            tempo = duracao_total

        # FINALIZADO (90%)
        finalizado = tempo >= int(duracao_total * 0.90)

        # BUSCAR HISTÓRICO
        historico = Historico.query.filter_by(
            usuario_id=usuario_id,
            tipo_midia=tipo,
            midia_id=midia_id
        ).first()

        if historico:
            historico.tempo_atual = tempo
            historico.finalizado = finalizado
        else:
            historico = Historico(
                usuario_id=usuario_id,
                tipo_midia=tipo,
                midia_id=midia_id,
                tempo_atual=tempo,
                finalizado=finalizado
            )
            db.session.add(historico)

        db.session.commit()
        return historico

  
    # CONTINUAR ASSISTINDO
   
    @staticmethod
    def listar_continuar(usuario_id, limite=10):
        return (
            Historico.query
            .filter_by(usuario_id=usuario_id, finalizado=False)
            .order_by(Historico.updated_at.desc())
            .limit(limite)
            .all()
        )

   
    # HISTÓRICO COMPLETO

    @staticmethod
    def listar_historico(usuario_id):
        return (
            Historico.query
            .filter_by(usuario_id=usuario_id)
            .order_by(Historico.updated_at.desc())
            .all()
        )
